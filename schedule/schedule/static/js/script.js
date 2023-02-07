function add_new_form(
    listName,
    hiddenElementId,
    clonedElementClassName, 
    totalNumberOfElementId,
    removeLineBtn,
    event) {
    if (event) {
      event.preventDefault()
    }
    const formCopyTarget = document.getElementById(listName)
    const currentCommlineForms = document.getElementsByClassName(clonedElementClassName)

    if (currentCommlineForms.length>=0) {
      removeLineBtn.setAttribute('class', '')
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

  