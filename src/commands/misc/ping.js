const { MessageEmbed } = require('discord.js');
const { colors } = require('../../config.json');

module.exports = {
    name: 'ping',
    description: '🏓 Pong !',
    run: (client, interaction) => {
        const replyEmbed = new MessageEmbed()
            .setColor(colors.base)
            .setTitle("🏓 Pong !")
            .setDescription(`\nLantence : \`${client.ws.ping}ms\``)
            .setFooter({
                text: `${client.user.username} | ping`,
                iconURL: client.user.displayAvatarURL()
            });

        interaction.reply({
            embeds: [replyEmbed],
            ephemeral: true
        });
    }
}