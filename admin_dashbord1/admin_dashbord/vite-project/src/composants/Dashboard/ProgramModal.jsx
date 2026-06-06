// Importation des hooks React et des styles
import React, { useState, useEffect } from 'react';
import './ProgramModal.css';
import { X } from 'lucide-react'; // Icône de fermeture

// Composant modal pour ajouter ou modifier un programme
const ProgramModal = ({ program, onClose, onSave }) => {
  // Définition des champs du formulaire liés à la table "programme"
  const [formData, setFormData] = useState({
    nom_programme: '',
    type_programme: '',
    description: '',
    date_debut: '',
    date_fin: '',
    lieu: '',
    capacite_max: '',
    statut: 'en_attente',
    date_creation: '',
    date_debut_recrutement: '',
    date_fin_recrutement: '',
    formulaire: '',
    id_utilisateur: ''
  });

  // Pré-remplissage si on est en mode édition
  useEffect(() => {
    if (program) {
      setFormData({
        nom_programme: program.nom_programme || '',
        type_programme: program.type_programme || '',
        description: program.description || '',
        date_debut: program.date_debut || '',
        date_fin: program.date_fin || '',
        lieu: program.lieu || '',
        capacite_max: program.capacite_max || 0,
        statut: program.statut || 'en_attente',
        date_creation: program.date_creation || '',
        date_debut_recrutement: program.date_debut_recrutement || '',
        date_fin_recrutement: program.date_fin_recrutement || '',
        formulaire: program.formulaire || '',
        id_utilisateur: program.id_utilisateur || ''
      });
    }
  }, [program]);

  // Mise à jour du state en cas de modification dans les champs
  const handleChange = (e) => {
    const { name, value } = e.target;
    const processedValue = name === 'capacite_max' ? parseInt(value) || 0 : value;
    setFormData({ ...formData, [name]: processedValue });
  };

  // Soumission du formulaire
  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData); // Envoie des données au parent
    onClose();         // Fermeture de la modale
  };

  // Évite que le clic intérieur ferme la modale
  const handleModalContentClick = (e) => {
    e.stopPropagation();
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content" onClick={handleModalContentClick}>
        {/* En-tête */}
        <header className="modal-header">
          <h2>{program ? 'Modifier le programme' : 'Nouveau Programme'}</h2>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </header>

        {/* Formulaire de saisie */}
        <form className="modal-form" id="programForm" onSubmit={handleSubmit}>
          {/* Nom */}
          <div className="form-group">
            <label htmlFor="nom_programme">Nom du programme</label>
            <input
              id="nom_programme"
              name="nom_programme"
              type="text"
              value={formData.nom_programme}
              onChange={handleChange}
              required
            />
          </div>

          {/* Type */}
          <div className="form-group">
            <label htmlFor="type_programme">Type de programme</label>
            <select
              id="type_programme"
              name="type_programme"
              value={formData.type_programme}
              onChange={handleChange}
              required
            >
              <option value="">-- Sélectionner --</option>
              <option value="court">Court</option>
              <option value="long">Long</option>
            </select>
          </div>

          {/* Description */}
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              rows="4"
              value={formData.description}
              onChange={handleChange}
              required
            ></textarea>
          </div>

          {/* Dates de début et fin */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="date_debut">Date de début</label>
              <input
                id="date_debut"
                name="date_debut"
                type="date"
                value={formData.date_debut}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="date_fin">Date de fin</label>
              <input
                id="date_fin"
                name="date_fin"
                type="date"
                value={formData.date_fin}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Recrutement */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="date_debut_recrutement">Début recrutement</label>
              <input
                id="date_debut_recrutement"
                name="date_debut_recrutement"
                type="date"
                value={formData.date_debut_recrutement}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="date_fin_recrutement">Fin recrutement</label>
              <input
                id="date_fin_recrutement"
                name="date_fin_recrutement"
                type="date"
                value={formData.date_fin_recrutement}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Lieu */}
          <div className="form-group">
            <label htmlFor="lieu">Lieu</label>
            <input
              id="lieu"
              name="lieu"
              type="text"
              value={formData.lieu}
              onChange={handleChange}
              required
            />
          </div>

          {/* Capacité et Statut */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="capacite_max">Capacité max</label>
              <input
                id="capacite_max"
                name="capacite_max"
                type="number"
                value={formData.capacite_max}
                onChange={handleChange}
                min=""
              />
            </div>
            <div className="form-group">
              <label htmlFor="statut">Statut</label>
              <select
                id="statut"
                name="statut"
                value={formData.statut}
                onChange={handleChange}
              >
                <option value="en_attente">En attente</option>
                <option value="actif">Actif</option>
                <option value="termine">Terminé</option>
                <option value="archive">Archivé</option>
              </select>
            </div>
          </div>

          {/* Métadonnées */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="date_creation">Date création</label>
              <input
                id="date_creation"
                name="date_creation"
                type="date"
                value={formData.date_creation}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="formulaire">UUID formulaire</label>
              <input
                id="formulaire"
                name="formulaire"
                type="text"
                value={formData.formulaire}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="id_utilisateur">ID utilisateur</label>
              <input
                id="id_utilisateur"
                name="id_utilisateur"
                type="number"
                value={formData.id_utilisateur}
                onChange={handleChange}
              />
            </div>
          </div>
        </form>

        {/* Boutons d'action */}
        <footer className="modal-actions">
          <button type="button" className="btn-modal btn-secondary-modal" onClick={onClose}>Annuler</button>
          <button type="submit" form="programForm" className="btn-modal btn-primary-modal">
            {program ? 'Enregistrer les modifications' : 'Créer le programme'}
          </button>
        </footer>
      </div>
    </div>
  );
};

export default ProgramModal;
