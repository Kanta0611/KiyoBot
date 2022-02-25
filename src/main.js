const { Client } = require("discord.js");
const { token } = require("./config.json");

const client = new Client({ intents: 1 });

require('./utils/handlers/eventUtil.js')(client);

client.login(token);