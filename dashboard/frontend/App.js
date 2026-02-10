import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Navbar, Spinner, Alert, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import PriceChart from './components/PriceChart';
import EventsList from './components/EventsList';
import SummaryStats from './components/SummaryStats';
import { fetchPrices, fetchEvents, fetchStats } from './services/api';

function App() {
  const [loading, setLoading] = useState(true);
  const [priceData, setPriceData] = useState([]);
  const [events, setEvents] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [dateRange, setDateRange] = useState({
    start: '2000-01-01',
    end: '2022-12-31'
  });

  useEffect(() => {
    loadData();
  }, [dateRange]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [prices, eventsData, statsData] = await Promise.all([
        fetchPrices(dateRange.start, dateRange.end),
        fetchEvents('all', dateRange.start, dateRange.end),
        fetchStats()
      ]);
      setPriceData(prices);
      setEvents(eventsData);
      setStats(statsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEventSelect = (event) => {
    setSelectedEvent(event);
  };

  const handleDateRangeChange = (newRange) => {
    setDateRange(newRange);
  };

  return (
    <div className="App">
      <Navbar bg="dark" variant="dark" expand="lg" className="mb-4 shadow">
        <Container>
          <Navbar.Brand href="#">
            <i className="bi bi-graph-up me-2"></i>
            Brent Oil Price Analysis Dashboard
          </Navbar.Brand>
          <Navbar.Text className="text-light">
            {stats ? `${stats.date_range.start} to ${stats.date_range.end}` : 'Loading...'}
          </Navbar.Text>
        </Container>
      </Navbar>

      <Container fluid>
        {loading ? (
          <div className="text-center py-5">
            <Spinner animation="border" variant="primary" />
            <p className="mt-3">Loading dashboard data...</p>
          </div>
        ) : (
          <>
            <Row className="mb-4">
              <Col>
                <SummaryStats stats={stats} />
              </Col>
            </Row>

            <Row className="mb-4">
              <Col lg={8}>
                <Card className="shadow-sm">
                  <Card.Header className="bg-primary text-white">
                    <h5 className="mb-0">Brent Oil Price History</h5>
                  </Card.Header>
                  <Card.Body>
                    <PriceChart 
                      data={priceData} 
                      events={events}
                      selectedEvent={selectedEvent}
                    />
                  </Card.Body>
                </Card>
              </Col>
              
              <Col lg={4}>
                <Card className="shadow-sm h-100">
                  <Card.Header className="bg-info text-white">
                    <h5 className="mb-0">Historical Events</h5>
                  </Card.Header>
                  <Card.Body className="p-0" style={{ overflowY: 'auto', maxHeight: '500px' }}>
                    <EventsList 
                      events={events} 
                      onSelect={handleEventSelect}
                      selectedEvent={selectedEvent}
                    />
                  </Card.Body>
                </Card>
              </Col>
            </Row>

            {selectedEvent && (
              <Row className="mb-4">
                <Col>
                  <Card className="shadow-sm">
                    <Card.Header className="bg-warning">
                      <h5 className="mb-0">Event Impact Analysis: {selectedEvent.name}</h5>
                    </Card.Header>
                    <Card.Body>
                      <EventImpactView event={selectedEvent} />
                    </Card.Body>
                  </Card>
                </Col>
              </Row>
            )}
          </>
        )}
      </Container>

      <footer className="mt-5 py-3 bg-light border-top">
        <Container>
          <Row>
            <Col md={6}>
              <h6>Birhan Energies</h6>
              <p className="text-muted small">
                Data-driven insights for energy sector stakeholders
              </p>
            </Col>
            <Col md={6} className="text-md-end">
              <p className="text-muted small mb-0">
                Data: Brent Crude Oil Prices (1987-2022)<br />
                Analysis: Bayesian Change Point Detection
              </p>
            </Col>
          </Row>
        </Container>
      </footer>
    </div>
  );
}

// Simple Event Impact View Component
const EventImpactView = ({ event }) => {
  return (
    <Row>
      <Col md={4}>
        <Card className="text-center">
          <Card.Body>
            <h6 className="text-muted">Event Date</h6>
            <h4>{new Date(event.date).toLocaleDateString()}</h4>
          </Card.Body>
        </Card>
      </Col>
      <Col md={4}>
        <Card className="text-center">
          <Card.Body>
            <h6 className="text-muted">Event Type</h6>
            <h4>
              <span className={`badge bg-${
                event.type === 'Geopolitical' ? 'danger' : 
                event.type === 'Financial' ? 'warning' : 
                event.type === 'Policy' ? 'primary' : 'secondary'
              }`}>
                {event.type}
              </span>
            </h4>
          </Card.Body>
        </Card>
      </Col>
      <Col md={4}>
        <Card className="text-center">
          <Card.Body>
            <h6 className="text-muted">Severity</h6>
            <h4>
              <span className={`badge bg-${
                event.severity === 'High' ? 'danger' : 
                event.severity === 'Medium' ? 'warning' : 'success'
              }`}>
                {event.severity}
              </span>
            </h4>
          </Card.Body>
        </Card>
      </Col>
    </Row>
  );
};

export default App;