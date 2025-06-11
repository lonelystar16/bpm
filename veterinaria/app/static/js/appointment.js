// Appointment form functionality

document.addEventListener("DOMContentLoaded", () => {
  initializeAppointmentForm()
  initializeServiceSelection()
  initializeDateTimeSelection()
  preSelectServiceFromURL()
})

let currentStep = 1
const totalSteps = 4

function initializeAppointmentForm() {
  const form = document.getElementById("appointment-form")
  const nextButtons = document.querySelectorAll(".next-step")
  const prevButtons = document.querySelectorAll(".prev-step")

  // Next step buttons
  nextButtons.forEach((button) => {
    button.addEventListener("click", () => {
      if (validateCurrentStep()) {
        nextStep()
      }
    })
  })

  // Previous step buttons
  prevButtons.forEach((button) => {
    button.addEventListener("click", () => {
      prevStep()
    })
  })

  // Form submission
  form.addEventListener("submit", (e) => {
    e.preventDefault()
    if (validateCurrentStep()) {
      submitAppointment()
    }
  })

  // Set minimum date to today
  const dateInput = document.getElementById("appointment-date")
  if (dateInput) {
    const today = new Date().toISOString().split("T")[0]
    dateInput.min = today
  }
}

function initializeServiceSelection() {
  const serviceRadios = document.querySelectorAll('input[name="service"]')
  const addressContainer = document.getElementById("address-container")

  serviceRadios.forEach((radio) => {
    radio.addEventListener("change", function () {
      // Show address field for mobile service
      if (this.value === "movil") {
        addressContainer.style.display = "block"
        document.getElementById("address").required = true
      } else {
        addressContainer.style.display = "none"
        document.getElementById("address").required = false
      }
    })
  })
}

function initializeDateTimeSelection() {
  const dateInput = document.getElementById("appointment-date")
  const timeSelect = document.getElementById("appointment-time")

  if (dateInput) {
    dateInput.addEventListener("change", function () {
      updateAvailableTimeSlots(this.value)
    })
  }
}

function preSelectServiceFromURL() {
  const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable
  const serviceParam = MascotaFeliz.getUrlParameter("servicio")
  if (serviceParam) {
    const serviceRadio = document.getElementById(`service-${serviceParam}`)
    if (serviceRadio) {
      serviceRadio.checked = true
      serviceRadio.dispatchEvent(new Event("change"))
    }
  }
}

function nextStep() {
  if (currentStep < totalSteps) {
    // Hide current step
    document.getElementById(`step${currentStep}`).classList.remove("active")
    document.getElementById(`step${currentStep}-indicator`).classList.remove("active")
    document.getElementById(`step${currentStep}-indicator`).classList.add("completed")

    // Show next step
    currentStep++
    document.getElementById(`step${currentStep}`).classList.add("active")
    document.getElementById(`step${currentStep}-indicator`).classList.add("active")

    // Update summary if on confirmation step
    if (currentStep === 4) {
      updateConfirmationSummary()
    }

    // Scroll to top of form
    document.querySelector(".appointment-stepper").scrollIntoView({
      behavior: "smooth",
    })
  }
}

function prevStep() {
  if (currentStep > 1) {
    // Hide current step
    document.getElementById(`step${currentStep}`).classList.remove("active")
    document.getElementById(`step${currentStep}-indicator`).classList.remove("active")

    // Show previous step
    currentStep--
    document.getElementById(`step${currentStep}`).classList.add("active")
    document.getElementById(`step${currentStep}-indicator`).classList.add("active")
    document.getElementById(`step${currentStep}-indicator`).classList.remove("completed")

    // Scroll to top of form
    document.querySelector(".appointment-stepper").scrollIntoView({
      behavior: "smooth",
    })
  }
}

function validateCurrentStep() {
  const currentStepElement = document.getElementById(`step${currentStep}`)
  const requiredFields = currentStepElement.querySelectorAll("[required]")
  let isValid = true

  requiredFields.forEach((field) => {
    if (!validateField(field)) {
      isValid = false
    }
  })

  // Additional validation for specific steps
  if (currentStep === 1) {
    const email = document.getElementById("owner-email").value
    const phone = document.getElementById("owner-phone").value

    if (!MascotaFeliz.validateEmail(email)) {
      showFieldError("owner-email", "Por favor ingresa un correo electrónico válido")
      isValid = false
    }

    if (!MascotaFeliz.validatePhone(phone)) {
      showFieldError("owner-phone", "Por favor ingresa un número de teléfono válido")
      isValid = false
    }
  }

  if (currentStep === 4) {
    const termsCheck = document.getElementById("terms-check")
    if (!termsCheck.checked) {
      MascotaFeliz.showNotification("Debes aceptar los términos y condiciones", "warning")
      isValid = false
    }
  }

  return isValid
}

function validateField(field) {
  const value = field.value.trim()

  if (field.hasAttribute("required") && !value) {
    showFieldError(field.id, "Este campo es obligatorio")
    return false
  }

  clearFieldError(field.id)
  return true
}

function showFieldError(fieldId, message) {
  const field = document.getElementById(fieldId)
  const existingError = field.parentNode.querySelector(".field-error")

  if (existingError) {
    existingError.remove()
  }

  const errorElement = document.createElement("div")
  errorElement.className = "field-error text-danger small mt-1"
  errorElement.textContent = message

  field.classList.add("is-invalid")
  field.parentNode.appendChild(errorElement)
}

function clearFieldError(fieldId) {
  const field = document.getElementById(fieldId)
  const existingError = field.parentNode.querySelector(".field-error")

  if (existingError) {
    existingError.remove()
  }

  field.classList.remove("is-invalid")
}

function updateAvailableTimeSlots(selectedDate) {
  const timeSelect = document.getElementById("appointment-time")
  const selectedDay = new Date(selectedDate).getDay()

  // Clear existing options
  timeSelect.innerHTML = '<option value="" selected disabled>Seleccionar horario</option>'

  // Define available time slots based on day
  let timeSlots = []

  if (selectedDay === 0) {
    // Sunday
    timeSlots = ["09:00", "10:00", "11:00"]
  } else if (selectedDay === 6) {
    // Saturday
    timeSlots = ["09:00", "10:00", "11:00", "12:00"]
  } else {
    // Monday to Friday
    timeSlots = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"]
  }

  // Add time slots to select
  timeSlots.forEach((time) => {
    const option = document.createElement("option")
    option.value = time
    option.textContent = MascotaFeliz.formatTime(time)
    timeSelect.appendChild(option)
  })
}

function updateConfirmationSummary() {
  // Get form data
  const ownerName = document.getElementById("owner-name").value
  const petName = document.getElementById("pet-name").value
  const petType = document.getElementById("pet-type").value
  const service = document.querySelector('input[name="service"]:checked')
  const address = document.getElementById("address").value
  const date = document.getElementById("appointment-date").value
  const time = document.getElementById("appointment-time").value

  // Update summary fields
  document.getElementById("summary-owner").textContent = ownerName
  document.getElementById("summary-pet").textContent = `${petName} (${petType})`

  if (service) {
    const serviceLabels = {
      clinica: "Consulta en clínica",
      movil: "Veterinaria móvil",
      peluqueria: "Peluquería",
      farmacia: "Farmacia",
    }
    document.getElementById("summary-service").textContent = serviceLabels[service.value]

    // Show address if mobile service
    const addressRow = document.getElementById("summary-address-row")
    if (service.value === "movil" && address) {
      document.getElementById("summary-address").textContent = address
      addressRow.style.display = "flex"
    } else {
      addressRow.style.display = "none"
    }
  }

  if (date && time) {
    const formattedDate = MascotaFeliz.formatDate(date)
    const formattedTime = MascotaFeliz.formatTime(time)
    document.getElementById("summary-datetime").textContent = `${formattedDate} a las ${formattedTime}`
  }
}

function submitAppointment() {
  const submitButton = document.querySelector('button[type="submit"]')
  MascotaFeliz.showLoading(submitButton)

  // Collect form data
  const appointmentData = {
    ownerName: document.getElementById("owner-name").value,
    ownerEmail: document.getElementById("owner-email").value,
    ownerPhone: document.getElementById("owner-phone").value,
    petName: document.getElementById("pet-name").value,
    petType: document.getElementById("pet-type").value,
    service: document.querySelector('input[name="service"]:checked').value,
    address: document.getElementById("address").value,
    date: document.getElementById("appointment-date").value,
    time: document.getElementById("appointment-time").value,
    comments: document.getElementById("comments").value,
    timestamp: new Date().toISOString(),
  }

  // Simulate API call
  setTimeout(() => {
    MascotaFeliz.hideLoading(submitButton)

    // Save appointment data to localStorage (for demo purposes)
    const appointments = MascotaFeliz.getFromStorage("appointments") || []
    appointments.push(appointmentData)
    MascotaFeliz.saveToStorage("appointments", appointments)

    // Show success modal
    const bootstrap = window.bootstrap // Declare bootstrap variable
    const successModal = new bootstrap.Modal(document.getElementById("successModal"))
    successModal.show()

    // Reset form
    document.getElementById("appointment-form").reset()
    currentStep = 1

    // Reset stepper
    document.querySelectorAll(".stepper-item").forEach((item) => {
      item.classList.remove("active", "completed")
    })
    document.getElementById("step1-indicator").classList.add("active")

    // Show first step
    document.querySelectorAll(".form-step").forEach((step) => {
      step.classList.remove("active")
    })
    document.getElementById("step1").classList.add("active")
  }, 2000) // Simulate 2 second delay
}

// Export functions for external use
window.AppointmentForm = {
  nextStep,
  prevStep,
  validateCurrentStep,
  updateConfirmationSummary,
}
