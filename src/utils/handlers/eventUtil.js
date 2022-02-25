const { promisify } = require('util');
const { glob } = require('glob');

const pGlob = promisify(glob);

module.exports = async client => {
    console.log("Debug 1");
    (await pGlob(`${process.cwd()}/src/events/*/*.js`)).map(eventFile => {
        const event = require(eventFile);
        console.log(`${event.name} chargé.`)

        if (event.once) {
            client.once(event.name, (...args) => event.execute(client, ...args));
        } else {
            client.on(event.name, (...args) => event.execute(client, ...args));
        }
    });
}