import React from 'react';

const StatsCard = ({ events, programs }) => {
  // Ex : un composant simple affichant quelques stats
  return (
    <div className="stats-card">
      <h2>Statistiques</h2>
      <p>Nombre d'événements : {events.length}</p>
      <p>Nombre de programmes : {programs.length}</p>
    </div>
  );
};

export default StatsCard;
