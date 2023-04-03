this.selectAllTests = function() {
    var checkboxes = document.getElementsByName('selected-tests');
    var selectAllCb = document.getElementsByName('select-all-tests');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = selectAllCb[0].checked
    }
 }
this.toggleSelectAllTests = function(){
    var selectAllCb = document.getElementsByName('select-all-tests');
    selectAllCb[0].checked = ""
}

this.changeHardwareAccelerationToggleValue = function(){
     var toggle = document.getElementsByName('toggle-hardware-acceleration')[0];
     if (toggle.checked)
        toggle.value="on"
     else
        toggle.value="off"
}