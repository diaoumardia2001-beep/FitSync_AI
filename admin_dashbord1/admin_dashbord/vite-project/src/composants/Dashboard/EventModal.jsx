import React, { useState, useEffect } from 'react';
import './EventModal.css';

// L'état initial reste le même pour la logique
const initialState = {
  nomEvenement: '', typeEvenement: '', description: '',
  dateDebut: '', dateFin: '', lieu: '',
  capaciteMax: '', administrateurId: '', affiche: null,
};

const EventModal = ({ event, onClose, onSave }) => {
  const [formData, setFormData] = useState(initialState);

  useEffect(() => {
    if (event) {
      const eventData = { ...initialState, ...event, affiche: null,
        dateDebut: event.dateDebut ? new Date(event.dateDebut).toISOString().slice(0, 16) : '',
        dateFin: event.dateFin ? new Date(event.dateFin).toISOString().slice(0, 16) : '',
      };
      setFormData(eventData);
    } else {
      setFormData(initialState);
    }
  }, [event]);

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    setFormData((prev) => ({ ...prev, [name]: type === 'file' ? files[0] : value }));
  };

  const handleSave = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const modalTitle = event ? 'Modifier un évènement' : 'Créer un évènement';

  // Le 'X' pour le bouton fermer
  const CloseIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );

  return (
    // Le fond flouté
    <div className="modal-backdrop" onClick={onClose}>
      {/* La nouvelle structure du modal */}
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        
        {/* 1. Header du Modal */}
        <div className="modal-header">
          <h2>{modalTitle}</h2>
          <button className="modal-close-btn" onClick={onClose} aria-label="Fermer">
            <CloseIcon />
          </button>
        </div>

        {/* 2. Corps du Modal (le formulaire) */}
        <form className="modal-form" onSubmit={handleSave}>
          <div className="form-group">
            <label htmlFor="nomEvenement">Nom de l'évènement</label>
            <input id="nomEvenement" name="nomEvenement" type="text" value={formData.nomEvenement} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label htmlFor="typeEvenement">Type d'évènement</label>
            <input id="typeEvenement" name="typeEvenement" type="text" value={formData.typeEvenement} onChange={handleChange} />
          </div>

          {/* Utilisation de "form-row" pour mettre les dates côte à côte */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="dateDebut">Date de début</label>
              <input id="dateDebut" name="dateDebut" type="datetime-local" value={formData.dateDebut} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label htmlFor="dateFin">Date de fin</label>
              <input id="dateFin" name="dateFin" type="datetime-local" value={formData.dateFin} onChange={handleChange} />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea id="description" name="description" value={formData.description} onChange={handleChange} />
          </div>

          {/* Autre "form-row" pour lieu et capacité */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="lieu">Lieu</label>
              <input id="lieu" name="lieu" type="text" value={formData.lieu} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label htmlFor="capaciteMax">Capacité maximale</label>
              <input id="capaciteMax" name="capaciteMax" type="number" min="0" value={formData.capaciteMax} onChange={handleChange} />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="administrateurId">ID de l'administrateur</label>
            <input id="administrateurId" name="administrateurId" type="text" value={formData.administrateurId} onChange={handleChange} />
          </div>

          <div className="form-group">
            <label htmlFor="affiche">Affiche de l'évènement</label>
            <label htmlFor="affiche" className="file-input-custom">
              <span>{formData.affiche ? formData.affiche.name : "Cliquez pour choisir un fichier"}</span>
              <div className="file-input-button">Parcourir</div>
            </label>
            <input id="affiche" name="affiche" type="file" accept="image/*" onChange={handleChange} className="file-input-hidden" />
          </div>
        </form>

        {/* 3. Footer du Modal (les actions) */}
        <div className="modal-actions">
          <button type="button" className="btn-modal btn-secondary-modal" onClick={onClose}>
            Annuler
          </button>
          <button type="button" className="btn-modal btn-primary-modal" onClick={handleSave}>
            Enregistrer
          </button>
        </div>
      </div>
    </div>
  );
};

export default EventModal;