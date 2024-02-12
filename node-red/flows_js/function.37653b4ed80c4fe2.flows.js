const Node = {
  "id": "37653b4ed80c4fe2",
  "type": "function",
  "z": "aa5f3f9006d25110",
  "name": "generate districts",
  "func": "",
  "outputs": 1,
  "noerr": 0,
  "initialize": "",
  "finalize": "",
  "libs": [],
  "x": 530,
  "y": 840,
  "wires": [
    [
      "8a67677275999751"
    ]
  ],
  "_order": 189
}

Node.func = async function (node, msg, RED, context, flow, global, env, util) {
  msg.payload = [
      { "vitacommDistrict": "Borgerteam Nordvest", "nexusDistrict": "Borgerteam Nordvest" },
      { "vitacommDistrict": "Borgerteams", "nexusDistrict": "Borgerteam Sydvest" },
      { "vitacommDistrict": "Åbakken", "nexusDistrict": "Distrikt Åbakken" },
      { "vitacommDistrict": "Bakkegaarden", "nexusDistrict": "Distrikt Bakkegården" },
      { "vitacommDistrict": "Borupvænget", "nexusDistrict": "Distrikt Borupvænget" },
      { "vitacommDistrict": "Dronningborg", "nexusDistrict": "Distrikt Dronningborg" },
      { "vitacommDistrict": "Kollektivhuset/Hornbæk", "nexusDistrict": "Distrikt Kollektivhuset" },
      { "vitacommDistrict": "Kristrup/Vorup", "nexusDistrict": "Distrikt Kristrup-Vorup" },
      { "vitacommDistrict": "Langå", "nexusDistrict": "Distrikt Langå" },
      { "vitacommDistrict": "Lindevænget", "nexusDistrict": "Distrikt Lindevænget" },
      { "vitacommDistrict": "Midtbyen", "nexusDistrict": "Distrikt Midtbyen" },
      { "vitacommDistrict": "Møllevang", "nexusDistrict": "Distrikt Møllevang" },
      { "vitacommDistrict": "Paderup/Assentoft", "nexusDistrict": "Distrikt Paderup-Assentoft" },
      { "vitacommDistrict": "Natcenter", "nexusDistrict": "Natcenter 8915 8833" },
      { "vitacommDistrict": "Plejecenter Bakkegaarden", "nexusDistrict": "Plejecenter Bakkegården" },
      { "vitacommDistrict": "Sygepleje nord", "nexusDistrict": "Sygeplejegrupper Nord" },
      { "vitacommDistrict": "Sygepleje syd", "nexusDistrict": "Sygeplejegrupper Syd" },
      { "vitacommDistrict": "Sygepleje vest", "nexusDistrict": "Sygeplejegrupper Vest" },
      { "vitacommDistrict": "Sundhed, Kultur og Omsorg", "nexusDistrict": "Intet distrikt"  }
  ]
  return msg;
}

module.exports = Node;