const poke1 = fetch("https://pokeapi.co/api/v2/pokemon/ditto");
const poke2 = fetch("https://pokeapi.co/api/v2/pokemon/charmander");
const poke3 = fetch("https://pokeapi.co/api/v2/pokemon/pikachu");

const all = Promise.all([poke1, poke2, poke3])
  .then((responses) => {
    return Promise.all(responses.map((res) => res.json()));
  })
  .then((data) => {
    data.forEach((pokemon) => {
      console.log(pokemon.name);
    });
  })
  .catch((error) => {
    console.log(`error: ${error}`);
  });
