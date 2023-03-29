function add_new_form(
    listName,
    hiddenElementId,
    clonedElementClassName, 
    totalNumberOfElementId,
    elementPrefix,
    brend_url,
    removeLineBtn,
    event) {
    if (event) {
      event.preventDefault()
    }

    const formCopyTarget = document.getElementById(listName)
    const currentCommlineForms = document.getElementsByClassName(clonedElementClassName)

    if (currentCommlineForms.length>=0) {
      removeLineBtn.setAttribute('class', 'button_add')
    }
    var addedFormCount = currentCommlineForms.length



    const copyemptyFormEl = document.getElementById(hiddenElementId).cloneNode(true)
    copyemptyFormEl.setAttribute('class', clonedElementClassName)
    copyemptyFormEl.setAttribute('id', `form-${addedFormCount}`)
    const regex = new RegExp('__prefix__', 'g')
    copyemptyFormEl.innerHTML = copyemptyFormEl.innerHTML.replace(regex, addedFormCount)
    const totalNewForms = document.getElementById(totalNumberOfElementId)
    totalNewForms.setAttribute('value', addedFormCount + 1)
    formCopyTarget.append(copyemptyFormEl)

    const startTimeId = `#${elementPrefix}-${addedFormCount}-start`
    const endTimeId = `#${elementPrefix}-${addedFormCount}-end`

    $(startTimeId).datetimepicker
    ({
      format:'Y-m-d H:i',
      step: 5
    });
    $(endTimeId).datetimepicker
    ({
      format:'Y-m-d H:i',
      step: 5
    });


    if (brend_url!==''){
      var typeId = `${elementPrefix}-${addedFormCount}-type`
      var confId = `${elementPrefix}-${addedFormCount}-type_player`
      var idOfSelect = $(`#${typeId}`)
      idOfSelect.change(function () {
        var url = $("#cfgForm").attr(brend_url);
        var recId = $(this).val();
        $.ajax({
          url: url,
          data: {
            'id': recId
          },
          success: function (data) {
            $(`#${confId}`).html(data);
          }
        });
      });
    }
  }

  function remove_form(
    listName,
    clonedElementClassName,
    totalNumberOfElementId,
    initialCount,
    removeLineBtn,
    event) {
    const currentCommlineForms = document.getElementsByClassName(clonedElementClassName)
    const totalNewForms = document.getElementById(totalNumberOfElementId)
    const formCopyTarget = document.getElementById(listName)
    if (event) {
      event.preventDefault()
    }

    var currentFormCount = currentCommlineForms.length-1

    const emptyFormEl = formCopyTarget.querySelector(`#form-${currentFormCount}`)
    currentFormCount = currentFormCount - 1
    emptyFormEl.remove()
    totalNewForms.setAttribute('value', currentFormCount + 1)
    console.log(initialCount)
    if (currentFormCount-initialCount<0) {
      removeLineBtn.setAttribute('class', 'hidden')
    }
  }
function showAddPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    href = triggeringLink.href;
    var win = window.open(href, name, 'height=300,width=400,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}
function closePopup(win, newID, newRepr, id) {
  console.log('jopa')
    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>')
    win.close();
}
