const { Client, Collection } = require("discord.js"); const client = new Client({ intents: 517 });
const { token } = require("./config.json");

client.commands = new Collection();

['eventUtil', 'commandUtil'].forEach(handler => {
    require(`./utils/handlers/${handler}.js`)(client);
});

process.on('unhandledRejection', (reason, promise) => {console.log(`UNHANDLED_REJECTION : ${reason}\n`, promise)});

client.login(token);