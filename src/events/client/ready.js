const { devGuildId } = require('../../config.json');

module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        client.user.setActivity(
            '/help | Morue salée',
            {
                type: 'WATCHING'
            }
        );
        console.log(`${client.user.username} est en ligne.`);
        
        // Instantané
        const devGuild = await client.guilds.cache.get(devGuildId);
        devGuild.commands.set(client.commands.map(command => command));

        // Global (1h min.)
        //TODO: Global slash commands push
    }
}