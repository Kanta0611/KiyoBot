module.exports = {
    name: "interactionCreate",
    once: false,
    async execute(client, interaction) {
        if (interaction.isCommand()) {
            const command = client.commands.get(interaction.commandName);
            if (!command) return interaction.reply("Commande obsolète");
            command.run(client, interaction);
        }
    }
}