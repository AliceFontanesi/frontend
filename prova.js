$(document).ready(function(){
    $.ajax({
        url: 'http://localhost:8000/products', // URL del tuo server Python che fornisce l'API JSON per i prodotti
        type: 'GET',
        success: function(response){
            console.log('Risposta ricevuta:', response); // Controllo: log della risposta ricevuta
            displayProducts(response); // Funzione per visualizzare i prodotti nella pagina HTML
        },
        error: function(xhr, status, error) {
            console.error('Errore:', error); // Gestione degli errori
        }
    });
});


function displayProducts(data) {
    var products = json.loads(data.decode('utf-8')); // Parsing dei dati JSON
    //manca foreach
    attributes = data['data']['attributes']
    marca = attributes.get('marca')
    nome = attributes.get('nome')
    prezzo = attributes.get('prezzo')
   
    var output = '<ul>';
    products.forEach(function(product) {
        output += '<li>ID: ' + product["id"] + ', Nome: ' + nome + ', Prezzo: ' + prezzo + ', Marca: ' + marca + '</li>';
    });
    output += '</ul>';
   
    // Inserimento dell'HTML nella pagina HTML
    document.write(output)
    $('#output').html(output);
}








/*function displayProducts(data) {
    var products = JSON.parse(data).data; // Parsing dei dati JSON
    console.log('Prodotti:', products); // Controllo: log dei prodotti
   
    // Costruzione dell'HTML per visualizzare i prodotti
    var output = '<ul>';
    products.forEach(function(product) {
        output += '<li>ID: ' + product["id"] + ', Nome: ' + product.attributes["nome"] + ', Prezzo: ' + product.attributes["prezzo"] + ', Marca: ' + product.attributes["marca"] + '</li>';
    });
    output += '</ul>';
   
    // Inserimento dell'HTML nella pagina HTML
    document.write(output)
    //$('#output').html(output);
}*/
