// Authentication functionality

document.addEventListener("DOMContentLoaded", () => {
  initializeAuthForms()
  initializePasswordToggles()
  initializeFormValidation()
})

function initializeAuthForms() {
  const loginForm = document.querySelector("#login-form form")
  const registerForm = document.querySelector("#register-form form")

  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin)
  }

  if (registerForm) {
    registerForm.addEventListener("submit", handleRegister)
  }
}

function initializePasswordToggles() {
  const toggleButtons = document.querySelectorAll('[id^="toggle-"]')

  toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const targetId = this.id.replace("toggle-", "")
      const passwordField = document.getElementById(targetId)
      const icon = this.querySelector("i")

      if (passwordField.type === "password") {
        passwordField.type = "text"
        icon.classList.remove("bi-eye")
        icon.classList.add("bi-eye-slash")
      } else {
        passwordField.type = "password"
        icon.classList.remove("bi-eye-slash")
        icon.classList.add("bi-eye")
      }
    })
  })
}

function initializeFormValidation() {
  // Real-time validation for register form
  const registerPassword = document.getElementById("register-password")
  const confirmPassword = document.getElementById("confirm-password")

  if (registerPassword && confirmPassword) {
    confirmPassword.addEventListener("input", () => {
      validatePasswordMatch()
    })

    registerPassword.addEventListener("input", () => {
      validatePasswordStrength()
      if (confirmPassword.value) {
        validatePasswordMatch()
      }
    })
  }

  // Email validation
  const emailInputs = document.querySelectorAll('input[type="email"]')
  emailInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      validateEmailField(this)
    })
  })

  // Phone validation
  const phoneInputs = document.querySelectorAll('input[type="tel"]')
  phoneInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      validatePhoneField(this)
    })
  })
}

function handleLogin(e) {
  e.preventDefault()

  const email = document.getElementById("login-email").value
  const password = document.getElementById("login-password").value
  const rememberMe = document.getElementById("remember-me").checked
  const submitButton = e.target.querySelector('button[type="submit"]')

  // Validate form
  if (!validateLoginForm(email, password)) {
    return
  }

  const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable
  MascotaFeliz.showLoading(submitButton)

  // Simulate API call
  setTimeout(() => {
    MascotaFeliz.hideLoading(submitButton)

    // Check credentials (demo purposes)
    const users = MascotaFeliz.getFromStorage("users") || []
    const user = users.find((u) => u.email === email && u.password === password)

    if (user) {
      // Successful login
      const sessionData = {
        user: {
          id: user.id,
          name: user.name,
          email: user.email,
          phone: user.phone,
        },
        loginTime: new Date().toISOString(),
        rememberMe: rememberMe,
      }

      MascotaFeliz.saveToStorage("currentUser", sessionData)
      MascotaFeliz.showNotification("¡Bienvenido de vuelta!", "success")

      // Redirect to profile or previous page
      setTimeout(() => {
        window.location.href = "perfil.html"
      }, 1500)
    } else {
      MascotaFeliz.showNotification("Credenciales incorrectas. Por favor verifica tu email y contraseña.", "danger")
    }
  }, 2000)
}

function handleRegister(e) {
  e.preventDefault()

  const formData = {
    name: document.getElementById("register-name").value,
    lastname: document.getElementById("register-lastname").value,
    email: document.getElementById("register-email").value,
    phone: document.getElementById("register-phone").value,
    password: document.getElementById("register-password").value,
  }

  const confirmPassword = document.getElementById("confirm-password").value
  const acceptTerms = document.getElementById("accept-terms").checked
  const submitButton = e.target.querySelector('button[type="submit"]')

  // Validate form
  if (!validateRegisterForm(formData, confirmPassword, acceptTerms)) {
    return
  }

  const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable
  MascotaFeliz.showLoading(submitButton)

  // Simulate API call
  setTimeout(() => {
    MascotaFeliz.hideLoading(submitButton)

    // Check if user already exists
    const users = MascotaFeliz.getFromStorage("users") || []
    const existingUser = users.find((u) => u.email === formData.email)

    if (existingUser) {
      MascotaFeliz.showNotification("Ya existe una cuenta con este correo electrónico.", "warning")
      return
    }

    // Create new user
    const newUser = {
      id: Date.now().toString(),
      ...formData,
      registrationDate: new Date().toISOString(),
    }

    users.push(newUser)
    MascotaFeliz.saveToStorage("users", users)

    MascotaFeliz.showNotification("¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.", "success")

    // Switch to login form
    setTimeout(() => {
      showLoginForm()
    }, 2000)
  }, 2000)
}

function validateLoginForm(email, password) {
  let isValid = true

  const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable

  if (!MascotaFeliz.validateEmail(email)) {
    showFieldError("login-email", "Por favor ingresa un correo electrónico válido")
    isValid = false
  } else {
    clearFieldError("login-email")
  }

  if (!MascotaFeliz.validateRequired(password)) {
    showFieldError("login-password", "La contraseña es obligatoria")
    isValid = false
  } else {
    clearFieldError("login-password")
  }

  return isValid
}

function validateRegisterForm(formData, confirmPassword, acceptTerms) {
  let isValid = true

  const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable

  // Validate required fields
  Object.keys(formData).forEach((key) => {
    const fieldId = `register-${key === "lastname" ? "lastname" : key}`
    if (!MascotaFeliz.validateRequired(formData[key])) {
      showFieldError(fieldId, "Este campo es obligatorio")
      isValid = false
    } else {
      clearFieldError(fieldId)
    }
  })

  // Validate email
  if (!MascotaFeliz.validateEmail(formData.email)) {
    showFieldError("register-email", "Por favor ingresa un correo electrónico válido")
    isValid = false
  }

  // Validate phone
  if (!MascotaFeliz.validatePhone(formData.phone)) {
    showFieldError("register-phone", "Por favor ingresa un número de teléfono válido")
    isValid = false
  }

  // Validate password strength
  if (!validatePasswordStrength()) {
    isValid = false
  }

  // Validate password match
  if (!validatePasswordMatch()) {
    isValid = false
  }

  // Validate terms acceptance
  if (!acceptTerms) {
    const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable
    MascotaFeliz.showNotification("Debes aceptar los términos y condiciones", "warning")
    isValid = false
  }

  return isValid
}

function validatePasswordStrength() {
  const password = document.getElementById("register-password").value
  const minLength = 8

  if (password.length < minLength) {
    showFieldError("register-password", `La contraseña debe tener al menos ${minLength} caracteres`)
    return false
  }

  clearFieldError("register-password")
  return true
}

function validatePasswordMatch() {
  const password = document.getElementById("register-password").value
  const confirmPassword = document.getElementById("confirm-password").value

  if (password !== confirmPassword) {
    showFieldError("confirm-password", "Las contraseñas no coinciden")
    return false
  }

  clearFieldError("confirm-password")
  return true
}

function validateEmailField(field) {
  const email = field.value

  const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable

  if (email && !MascotaFeliz.validateEmail(email)) {
    showFieldError(field.id, "Por favor ingresa un correo electrónico válido")
    return false
  }

  clearFieldError(field.id)
  return true
}

function validatePhoneField(field) {
  const phone = field.value

  const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable

  if (phone && !MascotaFeliz.validatePhone(phone)) {
    showFieldError(field.id, "Por favor ingresa un número de teléfono válido")
    return false
  }

  clearFieldError(field.id)
  return true
}

function showFieldError(fieldId, message) {
  const field = document.getElementById(fieldId)
  const inputGroup = field.closest(".input-group") || field.parentNode
  const existingError = inputGroup.parentNode.querySelector(".field-error")

  if (existingError) {
    existingError.remove()
  }

  const errorElement = document.createElement("div")
  errorElement.className = "field-error text-danger small mt-1"
  errorElement.textContent = message

  field.classList.add("is-invalid")
  inputGroup.parentNode.appendChild(errorElement)
}

function clearFieldError(fieldId) {
  const field = document.getElementById(fieldId)
  const inputGroup = field.closest(".input-group") || field.parentNode
  const existingError = inputGroup.parentNode.querySelector(".field-error")

  if (existingError) {
    existingError.remove()
  }

  field.classList.remove("is-invalid")
}

function showLoginForm() {
  document.getElementById("login-form").classList.add("active")
  document.getElementById("register-form").classList.remove("active")
}

function showRegisterForm() {
  document.getElementById("register-form").classList.add("active")
  document.getElementById("login-form").classList.remove("active")
}

// Check if user is logged in
function checkAuthStatus() {
  const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable
  const currentUser = MascotaFeliz.getFromStorage("currentUser")
  return currentUser && currentUser.user
}

// Logout function
function logout() {
  const MascotaFeliz = window.MascotaFeliz // Declare MascotaFeliz variable
  MascotaFeliz.removeFromStorage("currentUser")
  MascotaFeliz.showNotification("Sesión cerrada exitosamente", "info")
  window.location.href = "index.html"
}

// Export functions for external use
window.Auth = {
  showLoginForm,
  showRegisterForm,
  checkAuthStatus,
  logout,
}
