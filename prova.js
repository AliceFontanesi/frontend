document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:8000/products')
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella richiesta: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log('Risposta ricevuta:', data); // Controllo: log della risposta ricevuta
            displayProducts(data); // Funzione per visualizzare i prodotti nella pagina HTML
        })
        .catch(error => {
            console.error('Errore:', error); // Gestione degli errori
        });
});

function displayProducts(data) {
    var products = data.data; // Dati dei prodotti
    var output = '<ul>';
    products.forEach(function(product) {
        var attributes = product.attributes;
        var marca = attributes.marca;
        var nome = attributes.nome;
        var prezzo = attributes.prezzo;
        output += '<li>ID: ' + product.id + ', Nome: ' + nome + ', Prezzo: ' + prezzo + ', Marca: ' + marca + '</li>';
    });
    output += '</ul>';

    // Inserimento dell'HTML nella pagina HTML
    document.getElementById('output').innerHTML = output;
}
