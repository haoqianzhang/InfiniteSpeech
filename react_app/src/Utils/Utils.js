var bitcoin = require('bitcoinjs-lib')

function buildPost(txid, vout, amount, post) { 
    var value = amount*10e7    /* Need to be updated */
    op_return_data = Buffer.from(JSON.stringify(post), 'utf8')
    var alice = bitcoin.ECPair.fromWIF('5K48NE3WCt6mcAQur693L7QrpvjYLJkAuTX2jkvzLAit9LkJQRk')
    var txb = new bitcoin.TransactionBuilder()
    var dataScript = bitcoin.script.nullData.output.encode(op_return_data)

    txb.setVersion(2)
    txb.addInput(txid, vout) /* Need to be updated */
    txb.addOutput(dataScript, 0)
    txb.addOutput('1A6csP8jrpyruyW4a9tX9Nonv4R8AviB1y', value-10000)
    txb.sign(0, alice)
    console.log(txb.build().toHex())
}
