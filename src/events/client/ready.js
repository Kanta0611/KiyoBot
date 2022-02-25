module.exports = {
    name: 'ready',
    once: true,
    execute(client) {
        client.user.setActivity(
            '/help | Morue salée',
            {
                type: 'WATCHING'
            }
        );
        console.log(`${client.user.username} est en ligne.`);
    }
}