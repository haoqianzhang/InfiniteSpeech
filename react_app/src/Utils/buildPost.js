var bitcoin = require('bitcoinjs-lib')

function buildPost(txid, vout, amount, post) { 
    let value = amount*10e7    /* Need to be updated */
    let op_return_data = Buffer.from(JSON.stringify(post), 'utf8')
    let alice = bitcoin.ECPair.fromWIF('5K48NE3WCt6mcAQur693L7QrpvjYLJkAuTX2jkvzLAit9LkJQRk')
    let txb = new bitcoin.TransactionBuilder()
    let dataScript = bitcoin.script.nullData.output.encode(op_return_data)

    txb.setVersion(2)
    txb.addInput(txid, vout) /* Need to be updated */
    txb.addOutput(dataScript, 0)
    txb.addOutput('1A6csP8jrpyruyW4a9tX9Nonv4R8AviB1y', value - 10000)
    txb.sign(0, alice)
    return txb.build().toHex()
}

export default buildPost