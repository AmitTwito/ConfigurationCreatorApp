this.selectAll = function() {
    var checkboxes = document.getElementsByName('selected-tests');
    var selectAllCb = document.getElementsByName('select-all-tests');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = selectAllCb[0].checked
    }
 }
this.toggleSelectAll = function(){
    var selectAllCb = document.getElementsByName('select-all-tests');
    selectAllCb[0].checked = ""
}