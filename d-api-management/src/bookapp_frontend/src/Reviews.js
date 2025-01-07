import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Form, Row, Col } from 'react-bootstrap';

const Reviews = () => {
  const [reviews, setReviews] = useState([]);
  const [books, setBooks] = useState([]);
  const [newReview, setNewReview] = useState({ book_id: '', review_text: '', rating: 0 });

  useEffect(() => {
    fetchReviews();
    fetchBooks();
  }, []);

  const fetchReviews = async () => {
    try {
      const response = await axios.get('/api/reviews/');
      setReviews(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Error fetching reviews:', error);
      setReviews([]);
    }
  };

  const fetchBooks = async () => {
    const response = await axios.get('/api/books/');
    setBooks(response.data);
  };

  const handleChange = (e) => {
    setNewReview({ ...newReview, [e.target.name]: e.target.value });
  };

  const handleAddReview = async () => {
    try {
      await axios.post('/api/reviews/', newReview);
      fetchReviews();
      setNewReview({ book_id: '', review_text: '', rating: 0 });
    } catch (error) {
      console.error('Error adding review:', error);
    }
  };

  const handleDeleteReview = async (id) => {
    try {
      await axios.delete(`/api/reviews/${id}`);
      fetchReviews();
    } catch (error) {
      console.error('Error deleting review:', error);
    }
  };

  return (
    <div>
      <h1>Reviews</h1>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Book</th>
            <th>Review</th>
            <th>Rating</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {reviews.map((review) => {
            const book = books.find(b => b.id === review.book_id);
            return (
              <tr key={review.id}>
                <td>{book ? book.title : 'Unknown'}</td>
                <td>{review.review_text}</td>
                <td>{review.rating} stars</td>
                <td>
                  <Button variant="danger" onClick={() => handleDeleteReview(review.id)}>Delete</Button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </Table>
      <h2>Add a new review</h2>
      <Form>
        <Form.Group className="mb-3">
          <Form.Label>Book</Form.Label>
          <Form.Control as="select" name="book_id" value={newReview.book_id} onChange={handleChange}>
            <option value="">Select Book</option>
            {books.map((book) => (
              <option key={book.id} value={book.id}>{book.title}</option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Control type="text" name="review_text" value={newReview.review_text} onChange={handleChange} placeholder="Review Text" />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Control type="number" name="rating" value={newReview.rating} onChange={handleChange} placeholder="Rating" min="0" max="5" />
        </Form.Group>
        <Button variant="primary" onClick={handleAddReview}>Add Review</Button>
      </Form>
    </div>
  );
};

export default Reviews;
