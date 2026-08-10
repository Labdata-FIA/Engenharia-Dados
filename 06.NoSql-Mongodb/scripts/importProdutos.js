var produtos = [];

for (var i = 1; i <500; i++) {
    var idProduto = i + 1;

    var numSkus = Math.floor(Math.random() * 5) + 1;
    var skus = [];
    var idSkus = [];

    for (var j = 0; j < numSkus; j++) {
        var idSku = Math.floor(Math.random() * 90000) + 10000;
        idSkus.push(idSku);
        skus.push({
            idSku: idSku,
            nome: "Produto " + i + "-" + j,
            valor: Math.round((Math.random() * 5000 + 50) * 100) / 100,
            estoque: Math.floor(Math.random() * 50) + 1,
            cor: ["Vermelho", "Azul", "Verde", "Amarelo", "Preto"][Math.floor(Math.random() * 5)]
        });
    }

    var categorias = [];
    for (var k = 0; k < Math.floor(Math.random() * 3) + 1; k++) {
        categorias.push({
            idCategoria: Math.floor(Math.random() * 10) + 1,
            nome: "Categoria " + (Math.floor(Math.random() * 10) + 1)
        });
    }

    var imagens = [];
    for (var m = 0; m < Math.floor(Math.random() * 4) + 1; m++) {
        imagens.push({
            idImagem: Math.floor(Math.random() * 9000) + 1000,
            url: "https://example.com/img" + Math.floor(Math.random() * 100) + ".jpg"
        });
    }

    produtos.push({
        idProduto: idProduto,
        nomeProduto: "Produto " + i,
        valorProduto: Math.round((Math.random() * 10000 + 100) * 100) / 100,
        idSkus: idSkus, 
        skus: skus, 
        marcas: [{ idMarca: Math.floor(Math.random() * 50) + 1, nome: "Marca " + (Math.floor(Math.random() * 50) + 1) }],
        categorias: categorias,
        imagens: imagens
    });
}

db.produtos.insertMany(produtos);


print("✅ 500 produtos inseridos com sucesso!");