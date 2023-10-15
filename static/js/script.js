$('#addMediaBuying').on('hidden.bs.modal', function () {
    $(this)
      .find("input,textarea,select")
         .val('')
         .end()
      .find("input[type=checkbox], input[type=radio]")
         .prop("checked", "")
         .end();
})



document.getElementById("add_amount").addEventListener("keyup", add_convertToDollar);
document.getElementById("add_amount_dollar").addEventListener("keyup", add_convertToRiyal);

function add_convertToDollar() {
    let amount = document.getElementById("add_amount").value;
    document.getElementById("add_amount_dollar").value = Math.round((amount/3.75 + Number.EPSILON) * 100) / 100
    if (amount == '') {
    document.getElementById("add_amount_dollar").value = ''
    }
}


function add_convertToRiyal() {
    let amount_dollar = document.getElementById("add_amount_dollar").value;
    document.getElementById("add_amount").value = Math.round((amount_dollar*3.75 + Number.EPSILON) * 100) / 100
    if (amount_dollar == '') {
    document.getElementById("add_amount").value = ''
    }
}












