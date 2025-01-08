import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Form } from 'react-bootstrap';

const Books = () => {
  const [books, setBooks] = useState([]);
  const [newBook, setNewBook] = useState({ title: '', author: '', description: '' });

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const response = await axios.get('/api/books/');
      setBooks(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Error fetching books:', error);
      setBooks([]);
    }
  };

  const handleChange = (e) => {
    setNewBook({ ...newBook, [e.target.name]: e.target.value });
  };

  const handleAddBook = async () => {
    try {
      await axios.post('/api/books/', newBook);
      fetchBooks(); // Refresh the list
      setNewBook({ title: '', author: '', description: '' });
    } catch (error) {
      console.error('Error adding book:', error);
    }
  };

  const handleDeleteBook = async (id) => {
    try {
      await axios.delete(`/api/books/${id}`);
      fetchBooks();
    } catch (error) {
      console.error('Error deleting book:', error);
    }
  };

  return (
    <div>
      <h1>Books</h1>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {books.map((book) => (
            <tr key={book.id}>
              <td>{book.title}</td>
              <td>{book.author}</td>
              <td>{book.description}</td>
              <td>
                <Button variant="danger" onClick={() => handleDeleteBook(book.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
      <h2>Add a new book</h2>
      <Form>
        <Form.Group className="mb-3">
          <Form.Control type="text" name="title" value={newBook.title} onChange={handleChange} placeholder="Title" />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Control type="text" name="author" value={newBook.author} onChange={handleChange} placeholder="Author" />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Control type="text" name="description" value={newBook.description} onChange={handleChange} placeholder="Description" />
        </Form.Group>
        <Button variant="primary" onClick={handleAddBook}>Add Book</Button>
      </Form>
    </div>
  );
};

export default Books;
