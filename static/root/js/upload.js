/**
 * Created by Alessio on 05/10/2016.
 */


function Btn(id_btn,id_input) {
    document.getElementById(id_btn).onchange = function () {
        document.getElementById(id_input).value = this.value;
    };
}
