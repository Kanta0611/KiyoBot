const { MessageEmbed } = require('discord.js');

module.exports = {
    name: 'ping',
    description: '🏓 Pong !',
    run: (client, interaction) => {
        interaction.reply("Pong !");
    }
}