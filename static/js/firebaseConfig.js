// static/js/firebaseConfig.js

// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.3/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.12.3/firebase-analytics.js";
// Import Auth functions
import { 
  getAuth, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  sendPasswordResetEmail,
  onAuthStateChanged,
  signOut,
  updateProfile // <-- ADD THIS IMPORT
} from "https://www.gstatic.com/firebasejs/10.12.3/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA89tC5V5gj77dqH32i4BOKsaPCDBAA0NY",
  authDomain: "liver-tumor-detection.firebaseapp.com",
  projectId: "liver-tumor-detection",
  storageBucket: "liver-tumor-detection.firebasestorage.app",
  messagingSenderId: "154502791763",
  appId: "1:154502791763:web:5d317de198ddb0c6c03ca6",
  measurementId: "G-D1226HYVJL"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize and export Auth
export const auth = getAuth(app);

// Export all the functions we'll need
export { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  sendPasswordResetEmail,
  onAuthStateChanged,
  signOut,
  updateProfile // <-- ADD THIS EXPORT
};