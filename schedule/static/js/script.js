const changeTime = (time, timeCorrection) => {
  var newTime = new Date(time)
  newTime.setMinutes(newTime.getMinutes() + timeCorrection);
  var updateNewTimeString =   newTime.getFullYear() +
  '-' +
  ('0' + (newTime.getMonth() + 1)).slice(-2) +
  '-' +
  ('0' + newTime.getDate()).slice(-2) +
  ' ' +
  ('0' + newTime.getHours()).slice(-2) +
  ':' +
  ('0' + newTime.getMinutes()).slice(-2);
  return updateNewTimeString
};

var globalCamCount = 0;
var globalOpticsCount = 0;
var globalCamFormCount = 0;
var globalOpticsFormCount = 0;
var previusValuesDict = {}
const checkQuantityList = ['camera-form', 'optic-form'];

function sumQuantity(globalFormCount, elementPrefix) {
  var devicesCount = 0
  for (let i = 0; i < globalFormCount; i++) {
    const quantityField = `${elementPrefix}-${i}-quantity`
    devicesCount += parseInt(document.getElementById(quantityField).value, 10);
  }
  return devicesCount
}

function updateDateTimePicker(startTimeId, endTimeId, clonedElementClassName) {
  const timeRange = {
    'commline-form': [-20, 10],
    'techcommline-form': [-30, 20],
    'internetline-form': [-60, 20],
  };
  const timeStringStart = $('#id_broadcast_start_date').val();
  const updateStartTime = timeStringStart !== '' ? changeTime(timeStringStart, timeRange[clonedElementClassName][0]) : '';
  $(startTimeId).val(updateStartTime);

  const timeStringEnd = $('#id_broadcast_end_date').val();
  const updateEndTime = timeStringEnd !== '' ? changeTime(timeStringEnd, timeRange[clonedElementClassName][1]) : '';
  $(endTimeId).val(updateEndTime);

  $(document).ready(function () {
    $(startTimeId).datetimepicker({
      format: 'Y-m-d H:i',
      minDate: 0,
      step: 5,
      onShow: function () {
        this.setOptions({
          maxDate: $(endTimeId).val() ? $(endTimeId).val() : false,
        });
      },
    });
    $(endTimeId).datetimepicker({
      format: 'Y-m-d H:i',
      step: 5,
      onShow: function () {
        this.setOptions({
          minDate: $(startTimeId).val() ? $(startTimeId).val() : 0,
          value: $(endTimeId).val() ? $(endTimeId).val() : $(startTimeId).val() ? $(startTimeId).val() : 0,
        });
      },
    });
  });
}

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

    // Cameras - optics block
    if (checkQuantityList.includes(clonedElementClassName)) {
      if(elementPrefix === 'id_cameraptsconstructor_set')
        globalCamFormCount += 1;
      if(elementPrefix === 'id_opticptsconstructor_set')
        globalOpticsFormCount +=1;
      const inputId = `${elementPrefix}-${addedFormCount}-quantity`
      const input = document.getElementById(inputId);
      input.addEventListener('change', e => {
        if(elementPrefix === 'id_cameraptsconstructor_set')
          globalCamCount = sumQuantity(globalCamFormCount, elementPrefix)

        if(elementPrefix === 'id_opticptsconstructor_set')
          globalOpticsCount = sumQuantity(globalOpticsFormCount, elementPrefix)

        if(globalCamCount-globalOpticsCount <= 0)
          document.getElementById('add-more-optic').disabled = true;
        else
          document.getElementById('add-more-optic').disabled = false;

        if(globalCamCount-globalOpticsCount < 0 && elementPrefix === 'id_opticptsconstructor_set'){
          alert('Количество оптики не может превышать количество камер, будьте внимательней!');
          document.getElementById(inputId).value = previusValuesDict[inputId];
        }
        else if (elementPrefix === 'id_opticptsconstructor_set') previusValuesDict[inputId] = document.getElementById(inputId).value

        if(globalCamCount-globalOpticsCount < 0 && elementPrefix === 'id_cameraptsconstructor_set'){
          alert('Количество камер не может быть меньше количества оптики, будьте внимательней!');
          document.getElementById(inputId).value = previusValuesDict[inputId];
        }
        else if (elementPrefix === 'id_cameraptsconstructor_set') previusValuesDict[inputId] = document.getElementById(inputId).value

        console.log(previusValuesDict)
      });
    }
    // Cameras - optics block

    //Datetimepicker block
    const datetimepickerList = ['comm-id', 'tech-comm-id', 'internet-id'];

    if (datetimepickerList.includes(hiddenElementId)) {
      const startTimeId = `#${elementPrefix}-${addedFormCount}-start`
      const endTimeId = `#${elementPrefix}-${addedFormCount}-end`
      updateDateTimePicker(startTimeId, endTimeId, clonedElementClassName);
    }
    //Datetimepicker block

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
    

    // Cameras - optics block
    if (checkQuantityList.includes(clonedElementClassName)) {
      if(listName === 'camera-form-list'){
        lastCamVal = document.getElementById(`id_cameraptsconstructor_set-${currentFormCount}-quantity`).value; 
        if(globalCamCount-globalOpticsCount-lastCamVal < 0){
          alert('Следите за тем что б количетсво оптики не превышало количества камер');
          return
        }
        globalCamFormCount -= 1
        globalCamCount -= parseInt(lastCamVal, 10);
      }
      if(listName === 'optic-form-list'){
        globalOpticsFormCount -= 1
        lastOptVal = document.getElementById(`id_opticptsconstructor_set-${currentFormCount}-quantity`).value; 
        globalOpticsCount -= parseInt(lastOptVal, 10);
      }
    }
    // Cameras - optics block

    const emptyFormEl = formCopyTarget.querySelector(`#form-${currentFormCount}`)
    currentFormCount = currentFormCount - 1
    emptyFormEl.remove()
    totalNewForms.setAttribute('value', currentFormCount + 1)
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
    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>')
    win.close();
}
