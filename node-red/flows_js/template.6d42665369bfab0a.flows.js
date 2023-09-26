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
  "_order": 101
}

Node.template = `
const fileInput = document.getElementById('file');
const datetime = document.getElementById('datetime');
const filetype = document.getElementById('filetype');
const submit = document.getElementById('submit');

let now = new Date();
let time_offset = now.getMinutes() - now.getTimezoneOffset();
now.setMinutes(time_offset);
datetime.value = now.toISOString().slice(0, 16);

onchange = (e) => {
    if (fileInput.files.length > 0){
        let temp_fn = fileInput.files[0].name.split('.');
        temp_fn.pop();
        const file_name = temp_fn.join('.')
        if (file_name.includes('video')) {
            filetype.value = 'vitacomm';
        } else if (file_name.includes('Device_List')) {
            /* Moment not served when deployed - disabling for now
            // get time from default Knox file name
            let time_str = file_name.split("_").slice(-1);
            // moment libary added in html template
            let time_of_creation = moment(time_str, 'YYYY-MM-DD HH.mm.ss').format("YYYY-MM-DDTkk:mm").toString();
            datetime.value = time_of_creation
            */
            filetype.value = "knox";
        } else {
            filetype.value === 'unknown';
        }
    }

    datetime.type = filetype.value === "knox" ? 'datetime-local' : 'hidden';
    submit.disabled = filetype.value === "unknown" || fileInput.files.length < 1 ? true : false;
};
`

module.exports = Node;