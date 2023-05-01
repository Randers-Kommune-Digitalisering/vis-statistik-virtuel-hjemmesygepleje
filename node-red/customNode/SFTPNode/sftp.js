/**
 * Copyright 2015 Atsushi Kojo.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 **/

module.exports = function (RED)
{
    'use strict';
    //var sftp = require('ssh2-sftp-client');
    const sftp = require('ssh2').Client;
    var fs = require('fs');

    function SftpNode(n) {
        RED.nodes.createNode(this, n);
        var node = this;
        var credentials = RED.nodes.getCredentials(n.id);
        this.options = {
            'host': n.host || 'localhost',
            'port': n.port || 22,
            'forceIPv4': n.forceIPv4 || false,
            'forceIPv6': n.forceIPv6 || false,
            'username': n.username || 'anonymous',
            'password': this.credentials.password || '',
            'privateKey': n.privateKey && fs.readFileSync(n.privateKey) || '',
            'passphrase': this.credentials.passphrase || '',
            'agent': this.credentials.agent || '',
            'readyTimeout': n.readyTimeout || 20000,
            'strictVendor': n.strictVendor || true,
            'debug': new Function(n.debug) || '',
            'retries': n.retries || 2,
            'retry_factor': n.retry_factor || 2,
            'retry_minTimeout': n.retry_minTimeout || 2000
        };
    }

    RED.nodes.registerType('sftp', SftpNode,
    {
        credentials:
        {
            password: { type: 'password' },
            passphrase: { type: 'password' },
            agent: { type: 'text' }
        }
    });

    function SftpInNode(n)
    {
        RED.nodes.createNode(this, n);
        this.sftp = n.sftp;
        this.operation = n.operation;
        this.path = n.path;
        this.pattern = n.pattern;
        this.filename = n.filename;
        this.localFilename = n.localFilename;
        this.sftpConfig = RED.nodes.getNode(this.sftp);

        if (this.sftpConfig)
        {
            var node = this;
            node.on('input', function (msg)
            {
                /* Set SFTP settings from msg */
                var remotePath = msg.path || node.path || './';
                var pattern =  msg.pattern || node.pattern || '';

                var remoteFilename = msg.filename || node.filename || '';
                var remoteFilepath = remotePath + "/" + remoteFilename;

                var localFilename = msg.localfilename || msg.filename || node.localFilename || '';
                
                node.sftpConfig.options.host = msg.host || node.sftpConfig.options.host;
                node.sftpConfig.options.port = msg.port || node.sftpConfig.options.port;
                node.sftpConfig.options.username = msg.user || node.sftpConfig.options.username || '';
                node.sftpConfig.options.password = msg.password || node.sftpConfig.options.password || '';

                /* Establish connection */
                var conn = new sftp();

                this.sendMsg = function (err, result)
                {
                    console.log("Performing operation: " + node.operation);

                    if (err)
                    {
                        node.error(err, msg);
                        node.status({ fill: 'red', shape: 'ring', text: 'failed' });
                        return;
                    }

                    node.status({});

                    if (node.operation == 'get')
                    {
                        msg.payload = 'Get operation successful. ' + localFilename;
                    }
                    else if (node.operation == 'append')
                    {
                        msg.payload = 'Append operation successful. ' + remoteFilename;
                    }
                    else
                    {
                        msg.payload = result;
                    }

                    node.send(msg);
                };

                /* Operation functionality */
                conn.on('ready', function ()
                {
                    switch (node.operation)
                    {
                      
                      /* LIST */
                      case 'list':
                        conn.sftp(function (err, sftp)
                        {
                          if (err)
                          {
                            node.error(err, msg);
                            return;
                          }

                          sftp.readdir(remotePath, node.sendMsg);
                        });
                        break;

                      /* GET */
                      case 'get':
                        conn.sftp(function (err, sftp)
                        {
                          if (err)
                          {
                            node.error(err, msg);
                            return;
                          }

                          // Be very careful bufferSize too large causes issues with multi threading
                          let stream = sftp.createReadStream(remoteFilepath, { highWaterMark: 1024, bufferSize: 1024 });
        
                          let counter = 0;
                          let buf = '';
                          //let byteSize = 65536;
        
                          stream
                            .on('data', function (d)
                            {
                              buf += d;
                              counter++;

                              node.status({fill:"yellow",shape:"ring",text:("Downloading file ... ("+ counter + "): " + d.length + " Length: " + buf.length)});
                              // console.log("Read Chunk ("+ counter + "): " + d.length + " Length: " + buf.length);
                            })
                            .on('end', function ()
                            {
                              node.status({});
                              conn.end();

                              node.status({fill:"green",shape:"dot",text:"Download successful"});
                              // console.log('SFTP Read Chunks ' + counter + ' Length: ' + buf.length);
                              msg.payload = {};
                              msg.payload.filedata = buf;
                              node.send(msg);
                            });
                        });
                        break;

                      /* PUT */
                      case 'put':
                        conn.sftp(function (err, sftp)
                        {
                          if (err)
                          {
                            node.status({fill:"red",shape:"dot",text:"Error during PUT operation: " + err});
                            node.error(err, msg);
                            return;
                          }
                          let newFile = '';
                          if (msg.payload.filename)
                          {
                            newFile = msg.payload.filename;
                          }
                          else if (node.filename == '')
                          {
                            let d = new Date();
                            let guid = d.getTime().toString();
                            if (node.fileExtension == '')
                              node.fileExtension = '.txt';
                            newFile = node.remotePath + guid + node.fileExtension;
                          }
                          else
                          {
                            newFile = node.remotePath + node.filename;
                          }
        
                          let msgData = '';

                          if (msg.payload.filedata)
                            msgData = msg.payload.filedata;
                          else
                            msgData = JSON.stringify(msg.payload);
        
                          console.log('SFTP Put:' + newFile);
                          let writeStream = sftp.createWriteStream(newFile, { flags: 'w' });
                          
                          writeStream.write(msgData, function (err, result)
                          {
                            if(err)
                              node.status({fill:"red",shape:"dot",text:"Error during PUT operation: " + err});
                            else
                              node.status({fill:"green",shape:"dot",text:"PUT operation successful"});

                            conn.end();
                            msg.payload = {};
                            msg.payload.filename = newFile;
                            node.send(msg);
                          });
                        });
                        break;

                      /* DELETE */
                      case 'delete':
                        conn.sftp(function (err, sftp)
                        {
                          if (err)
                          {
                            node.error(err, msg);
                            return;
                          }
                          console.log('SFTP Deleting File: ' + remoteFilepath);
                          sftp.unlink(remoteFilepath, function (err)
                          {
                            if (err)
                            {
                              node.error(err, msg);
                              return;
                            }
                            else
                            {
                              console.log('SFTP file unlinked');
                              node.status({fill:"green",shape:"dot",text:"SFTP file unlinked successfully"});
                              msg.payload = {};
                              node.send(msg);
                            }
                            conn.end();
                          });
                        });
                        break;
                    } /* switch end */

                  }); /* conn.on() end */

                  conn.on('error', function (error) {
                    node.status({fill:"red",shape:"dot",text:"Connection error: " + error});
                    node.error(error, msg);
                    return;
                  });

                  conn.connect(node.sftpConfig.options);

            }); // Node.on() end
        }
        else
        {
            node.status({fill:"red",shape:"dot",text:"Missing SFTP configuration"});
            this.error('Missing SFTP configuration. Either config msg-object or directly in the node configuration.');
        }
    }
    RED.nodes.registerType('sftp in', SftpInNode);
}