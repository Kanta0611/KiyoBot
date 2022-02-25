const { promisify } = require('util');
const { glob } = require('glob');

const pGlob = promisify(glob);

module.exports = async client => {

    (await pGlob(`${process.cwd()}/src/commands/*/*.js`)).map(commandFile => {
        const command = require(commandFile);
        console.log(`${command.name} chargée.`);
        
        if (!command.name || !command.description) return console.log(`Commande non chargée : pas de nom ou de description. Fichier -> ${commandFile}`)
        client.commands.set(command.name, command);
    });
}