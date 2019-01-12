function create_table_for_document(aggregated, percentages) {
    var html = `
    <table>
    <tr>
        <td> </td>
        <td>equity_type: ___</td>
        <td>stocks__________</td>
        <td>bonds___________</td>
        <td>cash</td>
    </tr>
    <tr>
        <td>currency        </td>
        <td> </td>
        <td>${aggregated['stock'].toFixed(2)} (${percentages['stock'].toFixed(0)}%) </td>
        <td>${aggregated['bond'].toFixed(2)} (${percentages['bond'].toFixed(0)}%) </td>
        <td>${aggregated['cash'].toFixed(2)} (${percentages['cash'].toFixed(0)}%) </td>

    </tr>
    <tr>
        <td>USD</td>
        <td>15(30%)</td>
        <td>хз</td>
        <td>хз</td>
        <td>хз</td>
    </tr>
    <tr>
        <td>RUR</td>
        <td>35(70%)</td>
        <td>хз</td>
        <td>хз</td>
        <td>хз</td>
    </tr>
</table>
`
    var table = document.createElement('table')
    table.innerHTML = html
    return table
}

function add_to_header(el){
    var header = document.querySelector('[data-qa-file="BrokerAccountsHeaderPure"]')
    header.appendChild(el)
}

var aggregated = {
    bond: 151884.99407407406,
    cash: 1542.6000000000001,
    rub: 412632.9285185185,
    stock: 328234.4085185185,
    total: 481662.00259259256,
    usd: 69029.07407407406
}
var percentages = {
    bond: 31.53352210814603,
    cash: 0.32026607697862933,
    rub: 85.66856557035466,
    stock: 68.14621181487535,
    usd: 14.331434429645343
}

var table = create_table_for_document(aggregated, percentages)
add_to_header(table)