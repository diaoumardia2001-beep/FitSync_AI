// Importation des hooks React et des styles
import React, { useState, useEffect } from 'react';
import './AdminDashboard.css';

// Importation des icônes
import {
  Calendar,
  Play,
  BarChart3,
  Plus,
  Edit,
  Trash2,
  Clock,
  Users,
  Image as ImageIcon
} from 'lucide-react';

// Composants internes - VÉRIFIEZ CES IMPORTS
import EventModal from './EventModal';
import ProgramModal from './ProgramModal'; // Assurez-vous que ce fichier existe et est correct
import StatsCard from './StatsCard';

// API services
import {
  getAllEvents,
  createEvent,
  updateEvent,
  deleteEvent,
  getAllPrograms,
  createProgram,
  updateProgram,
  deleteProgram
} from "../../services/api";

// Composant principal
const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('events');
  const [events, setEvents] = useState([]);
  const [programs, setPrograms] = useState([]);
  const [showEventModal, setShowEventModal] = useState(false);
  const [showProgramModal, setShowProgramModal] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [selectedProgram, setSelectedProgram] = useState(null);

  useEffect(() => {
    fetchEvents();
    fetchPrograms();
  }, []);

  const fetchEvents = async () => {
    try {
      const res = await getAllEvents();
      setEvents(res.data);
    } catch (err) {
      console.error('Erreur chargement événements:', err);
    }
  };

  const fetchPrograms = async () => {
    try {
      const res = await getAllPrograms();
      console.log("Données programmes :", res.data); // debug
      setPrograms(res.data);
    } catch (err) {
      console.error('Erreur chargement programmes:', err);
    }
  };

  const saveEvent = async (eventData) => {
    try {
      if (selectedEvent) {
        await updateEvent(selectedEvent.id_evenement, eventData);
      } else {
        await createEvent(eventData);
      }
      fetchEvents();
      setSelectedEvent(null);
    } catch (err) {
      console.error('Erreur sauvegarde événement:', err);
    }
  };

  const saveProgram = async (programData) => {
    try {
      if (selectedProgram) {
        await updateProgram(selectedProgram.id_programme, programData);
      } else {
        await createProgram(programData);
      }
      fetchPrograms();
      setSelectedProgram(null);
    } catch (err) {
      console.error('Erreur sauvegarde programme:', err);
    }
  };

  const handleDeleteEvent = async (id) => {
    if (window.confirm("Supprimer cet événement ?")) {
      try {
        await deleteEvent(id);
        fetchEvents();
      } catch (err) {
        console.error('Erreur suppression événement:', err);
      }
    }
  };

  const handleDeleteProgram = async (id) => {
    if (window.confirm("Supprimer ce programme ?")) {
      try {
        await deleteProgram(id);
        fetchPrograms();
      } catch (err) {
        console.error('Erreur suppression programme:', err);
      }
    }
  };

  // Fonction pour ouvrir le modal programme
  const handleOpenProgramModal = () => {
    console.log("Ouverture du modal programme"); // Debug
    setSelectedProgram(null);
    setShowProgramModal(true);
    setShowEventModal(false); // S'assurer que le modal événement est fermé
  };

  // Fonction pour ouvrir le modal événement
  const handleOpenEventModal = () => {
    console.log("Ouverture du modal événement"); // Debug
    setSelectedEvent(null);
    setShowEventModal(true);
    setShowProgramModal(false); // S'assurer que le modal programme est fermé
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'planifié': return 'status-planned';
      case 'en_cours': return 'status-ongoing';
      case 'terminé': return 'status-finished';
      case 'annulé': return 'status-canceled';
      case 'actif': return 'status-active';
      case 'en_attente': return 'status-pending';
      default: return 'status-unknown';
    }
  };

  return (
    <div className="admin-dashboard">
      {/* En-tête */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Dashboard Administrateur</h1>
          <p>Gestion des événements et programmes</p>
        </div>
      </header>

      {/* Navigation */}
      <div className="dashboard-container">
        <nav className="dashboard-nav">
          {['events', 'programs', 'stats'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`nav-button ${activeTab === tab ? 'active' : ''}`}
            >
              {tab === 'events' && <><Calendar size={18} /> Événements</>}
              {tab === 'programs' && <><Play size={18} /> Programmes</>}
              {tab === 'stats' && <><BarChart3 size={18} /> Statistiques</>}
            </button>
          ))}
        </nav>

        {/* Contenu principal */}
        <main className="dashboard-main">
          {/* Événements */}
          {activeTab === 'events' && (
            <section className="content-section">
              <div className="section-header">
                <h2>Gestion des Événements</h2>
                <button className="btn btn-primary" onClick={handleOpenEventModal}>
                  <Plus size={16} /> Nouvel événement
                </button>
              </div>

              <div className="table-container">
                <table className="events-table">
                  <thead>
                    <tr>
                      <th>Affiche</th>
                      <th>Événement</th>
                      <th>Date & Heure</th>
                      <th>Statut</th>
                      <th>Participants</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {events.map((event) => (
                      <tr key={event.id_evenement}>
                        <td>
                          {event.affiche ? (
                            <img src={event.affiche} alt={event.nom_evenement} className="event-thumbnail" />
                          ) : (
                            <div className="event-thumbnail-placeholder"><ImageIcon size={20} /></div>
                          )}
                        </td>
                        <td>
                          <div className="event-title">{event.nom_evenement}</div>
                          <div className="event-type">{event.type_evenement}</div>
                        </td>
                        <td>
                          <div className="info-with-icon">
                            <Calendar size={14} />
                            {new Date(event.date_debut).toLocaleDateString('fr-FR')}
                          </div>
                          {event.date_fin && (
                            <div className="info-with-icon">
                              <Clock size={14} />
                              Fin: {new Date(event.date_fin).toLocaleDateString('fr-FR')}
                            </div>
                          )}
                        </td>
                        <td>{event.lieu}</td>
                        <td>{event.capacite_max}</td>
                        <td>{event.description}</td>
                        <td>{event.administrateur_id}</td>
                        <td>
                          <span className={`status-badge ${getStatusClass('actif')}`}>
                            Actif
                          </span>
                        </td>
                        <td>
                          <div className="info-with-icon"><Users size={14} /> 0</div>
                        </td>
                        <td>
                          <button className="btn-icon btn-edit" onClick={() => { setSelectedEvent(event); setShowEventModal(true); }}>
                            <Edit size={16} />
                          </button>
                          <button className="btn-icon btn-delete" onClick={() => handleDeleteEvent(event.id)}>
                            <Trash2 size={16} />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {/* Programmes */}
          {activeTab === 'programs' && (
            <section className="content-section">
              <div className="section-header">
                <h2>Gestion des Programmes</h2>
                <button className="btn btn-primary" onClick={handleOpenProgramModal}>
                  <Plus size={16} /> Nouveau programme
                </button>
              </div>

              <div className="programs-table-container">
                <table className="programs-table">
                  <thead>
                    <tr>
                      <th>Nom</th>
                      <th>Date début</th>
                      <th>Date fin</th>
                      <th>Début recrutement</th>
                      <th>Fin recrutement</th>
                      <th>Capacité</th>
                      <th>Statut</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {programs.map((program) => (
                      <tr key={program.id_programme}>
                        <td>{program.nom_programme}</td>
                        <td>{program.date_debut ? new Date(program.date_debut).toLocaleDateString('fr-FR') : 'N/A'}</td>
                        <td>{program.date_fin ? new Date(program.date_fin).toLocaleDateString('fr-FR') : 'N/A'}</td>
                        <td>{program.date_debut_recrutement ? new Date(program.date_debut_recrutement).toLocaleDateString('fr-FR') : '—'}</td>
                        <td>{program.date_fin_recrutement ? new Date(program.date_fin_recrutement).toLocaleDateString('fr-FR') : '—'}</td>
                        <td>{program.capacite_max}</td>
                        <td>
                          <span className={`status-badge ${getStatusClass(program.statut)}`}>
                            {program.statut.replace('_', ' ')}
                          </span>
                        </td>
                        <td>
                          <button className="btn-icon btn-edit" onClick={() => { setSelectedProgram(program); setShowProgramModal(true); }}>
                            <Edit size={18} />
                          </button>
                          <button className="btn-icon btn-delete" onClick={() => handleDeleteProgram(program.id_programme)}>
                            <Trash2 size={18} />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {/* Statistiques */}
          {activeTab === 'stats' && (
            <section className="content-section">
              <div className="section-header"><h2>Statistiques Générales</h2></div>
              <StatsCard events={events} programs={programs} />
            </section>
          )}
        </main>
      </div>

      {/* Modales - Ajout de debug */}
      {showEventModal && (
        <EventModal
          event={selectedEvent}
          onClose={() => { 
            console.log("Fermeture modal événement"); // Debug
            setShowEventModal(false); 
            setSelectedEvent(null); 
          }}
          onSave={saveEvent}
        />
      )}

      {showProgramModal && (
        <ProgramModal
          program={selectedProgram}
          onClose={() => { 
            console.log("Fermeture modal programme"); // Debug
            setShowProgramModal(false); 
            setSelectedProgram(null); 
          }}
          onSave={saveProgram}
        />
      )}
    </div>
  );
};

export default AdminDashboard;