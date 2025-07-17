import axios from 'axios';

//  Définis ici l'URL de base de ton API Spring Boot
const API_BASE_URL = 'http://192.168.252.101:8080';

// ===================== ÉVÉNEMENTS =====================

// Récupérer tous les événements
export const getAllEvents = () => axios.get(`${API_BASE_URL}/evenements`);

// Créer un nouvel événement
export const createEvent = (eventData) => axios.post(`${API_BASE_URL}/evenements`, eventData);

// Mettre à jour un événement existant
export const updateEvent = (id, eventData) => axios.put(`${API_BASE_URL}/evenements/${id}`, eventData);

// Supprimer un événement
export const deleteEvent = (id) => axios.delete(`${API_BASE_URL}/evenements/${id}`);


// ===================== PROGRAMMES =====================

// Récupérer tous les programmes
export const getAllPrograms = () => axios.get(`${API_BASE_URL}/programmes`);

// Créer un nouveau programme
export const createProgram = (programData) => axios.post(`${API_BASE_URL}/programmes`, programData);

// Mettre à jour un programme existant
export const updateProgram = (id, programData) => axios.put(`${API_BASE_URL}/programmes/${id}`, programData);

// Supprimer un programme
export const deleteProgram = (id) => axios.delete(`${API_BASE_URL}/programmes/${id}`);
