// static/js/auth.js

import { 
  auth, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  sendPasswordResetEmail,
  onAuthStateChanged,
  updateProfile // <-- ADD THIS IMPORT
} from './firebaseConfig.js';

// --- Check if user is already logged in ---
onAuthStateChanged(auth, (user) => {
  if (user) {
    window.location.href = '/'; // Redirect to the main dashboard
  }
});

// --- Handle Login Form ---
const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = loginForm.email.value;
    const password = loginForm.password.value;
    const errorEl = document.getElementById('error-message');

    try {
      await signInWithEmailAndPassword(auth, email, password);
      // Success! The onAuthStateChanged listener will handle the redirect.
    } catch (error) {
      errorEl.textContent = error.message;
      errorEl.style.display = 'block';
    }
  });
}

// --- Handle Signup Form (UPDATED) ---
const signupForm = document.getElementById('signup-form');
if (signupForm) {
  signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = signupForm.name.value; // <-- GET THE NAME
    const email = signupForm.email.value;
    const password = signupForm.password.value;
    const errorEl = document.getElementById('error-message');

    try {
      // Step 1: Create the user
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      
      // Step 2: Update their profile with the name
      await updateProfile(auth.currentUser, {
        displayName: name
      });
      
      // Success! The onAuthStateChanged listener will handle the redirect.
    } catch (error) {
      errorEl.textContent = error.message;
      errorEl.style.display = 'block';
    }
  });
}

// --- Handle Forgot Password Form ---
const forgotPasswordForm = document.getElementById('forgot-password-form');
if (forgotPasswordForm) {
  forgotPasswordForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = forgotPasswordForm.email.value;
    const errorEl = document.getElementById('error-message');
    const successEl = document.getElementById('success-message');

    try {
      await sendPasswordResetEmail(auth, email);
      errorEl.style.display = 'none';
      successEl.style.display = 'block';
      successEl.textContent = 'Password reset email sent! Check your inbox.';
    } catch (error) {
      successEl.style.display = 'none';
      errorEl.textContent = error.message;
      errorEl.style.display = 'block';
    }
  });
}