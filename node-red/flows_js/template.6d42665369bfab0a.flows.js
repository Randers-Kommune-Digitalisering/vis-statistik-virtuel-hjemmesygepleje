const Node = {
  "id": "6d42665369bfab0a",
  "type": "template",
  "z": "39989dadda5c9a15",
  "g": "b95d463f67a7a194",
  "name": "Javascript",
  "field": "payload.js",
  "fieldType": "msg",
  "format": "javascript",
  "syntax": "mustache",
  "template": "",
  "output": "str",
  "x": 300,
  "y": 80,
  "wires": [
    [
      "3153fbd3.203a64"
    ]
  ],
  "_order": 98
}

Node.template = `
const fileInput = document.getElementById('file');
const datetime = document.getElementById('datetime');
const filetype = document.getElementById('filetype');
const submit = document.getElementById('submit');

var now = new Date();
//now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
datetime.value = now.toString().slice(0, 16);

console.log(now.toISOString().slice(0, 16))

onchange = (e) => {
    if (fileInput.files.length > 0){
        let temp_fn = fileInput.files[0].name.split('.');
        temp_fn.pop();
        const file_name = temp_fn.join('.')
        if (file_name.includes('video')) {
            filetype.value = 'vitacomm';
        } else if (file_name.includes('Device_List')) {
            // get time from default Knox file name
            let time_str = file_name.split("_").slice(-1);
            // moment libary added in html template
            console.log(time_str)
            let time_of_creation = moment(time_str, 'YYYY-MM-DD HH.mm.ss').toString().slice(0, 16);
            console.log(time_of_creation)
            datetime.value = time_of_creation
            filetype.value = "knox";
        } else {
            filetype.value === 'unknown';
        }

        datetime.type = filetype.value === "knox" ? 'datetime-local' : 'hidden';        
        submit.disabled = filetype.value === "unknown" ? true :  false;
    }
};
`

module.exports = Node;