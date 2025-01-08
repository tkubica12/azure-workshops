import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Form } from 'react-bootstrap';

const Lists = () => {
  const [lists, setLists] = useState([]);
  const [books, setBooks] = useState([]);
  const [newList, setNewList] = useState({ name: '', description: '', books: [] });

  useEffect(() => {
    fetchLists();
    fetchBooks();
  }, []);

  const fetchLists = async () => {
    try {
      const response = await axios.get('/api/lists/');
      setLists(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Error fetching lists:', error);
      setLists([]);
    }
  };

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
    const { name, value } = e.target;
    if (name === 'books') {
      const selectedBooks = Array.from(e.target.selectedOptions, (option) => option.value);
      setNewList({ ...newList, books: selectedBooks });
    } else {
      setNewList({ ...newList, [name]: value });
    }
  };

  const handleAddList = async () => {
    try {
      await axios.post('/api/lists/', newList);
      fetchLists();
      setNewList({ name: '', description: '', books: [] });
    } catch (error) {
      console.error('Error adding list:', error);
    }
  };

  const handleDeleteList = async (id) => {
    try {
      await axios.delete(`/api/lists/${id}`);
      fetchLists();
    } catch (error) {
      console.error('Error deleting list:', error);
    }
  };

  return (
    <div>
      <h1>Lists</h1>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Books</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {lists.map((list) => (
            <tr key={list.id}>
              <td>{list.name}</td>
              <td>{list.description}</td>
              <td>
                {list.books.map(bookId => {
                  const book = books.find(b => b.id === bookId);
                  return book ? book.title : 'Unknown';
                }).join(', ')}
              </td>
              <td>
                <Button variant="danger" onClick={() => handleDeleteList(list.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
      <h2>Add a new list</h2>
      <Form>
        <Form.Group className="mb-3">
          <Form.Control type="text" name="name" value={newList.name} onChange={handleChange} placeholder="Name" />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Control type="text" name="description" value={newList.description} onChange={handleChange} placeholder="Description" />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Books</Form.Label>
          <Form.Control as="select" name="books" multiple value={newList.books} onChange={handleChange}>
            {books.map((book) => (
              <option key={book.id} value={book.id}>{book.title}</option>
            ))}
          </Form.Control>
        </Form.Group>
        <Button variant="primary" onClick={handleAddList}>Add List</Button>
      </Form>
    </div>
  );
};

export default Lists;
