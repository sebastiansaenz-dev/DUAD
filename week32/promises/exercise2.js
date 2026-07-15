const poke1 = fetch("https://pokeapi.co/api/v2/pokemon/ditto");
const poke2 = fetch("https://pokeapi.co/api/v2/pokemon/charmander");
const poke3 = fetch("https://pokeapi.co/api/v2/pokemon/pikachu");

const all = Promise.any([poke2, poke1, poke3])
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data.name);
  })
  .catch((error) => {
    console.log(`error: ${error}`);
  });
