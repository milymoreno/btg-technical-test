import { render, screen, fireEvent } from '@testing-library/react';
import UserList from './UserList';
import { describe, it, expect, vi } from 'vitest';

describe('UserList component', () => {
  const mockUsers = [
    { id: '1', name: 'John Doe', email: 'john@example.com' },
    { id: '2', name: 'Jane Smith', email: 'jane@example.com' },
  ];

  it('renders without crashing and shows empty state', () => {
    render(<UserList users={[]} onEdit={vi.fn()} onDelete={vi.fn()} />);
    
    expect(screen.getByText('Users Directory')).toBeInTheDocument();
    expect(screen.getByText('0 total')).toBeInTheDocument();
    expect(screen.getByText(/No users found/i)).toBeInTheDocument();
  });

  it('renders a list of users', () => {
    render(<UserList users={mockUsers} onEdit={vi.fn()} onDelete={vi.fn()} />);
    
    expect(screen.getByText('2 total')).toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText('jane@example.com')).toBeInTheDocument();
  });

  it('calls onEdit when the edit button is clicked', () => {
    const onEditMock = vi.fn();
    render(<UserList users={mockUsers} onEdit={onEditMock} onDelete={vi.fn()} />);
    
    // Get the first edit button (for John Doe)
    const editButtons = screen.getAllByTitle('Edit');
    fireEvent.click(editButtons[0]);
    
    expect(onEditMock).toHaveBeenCalledTimes(1);
    expect(onEditMock).toHaveBeenCalledWith(mockUsers[0]);
  });

  it('calls onDelete when the delete button is clicked', () => {
    const onDeleteMock = vi.fn();
    render(<UserList users={mockUsers} onEdit={vi.fn()} onDelete={onDeleteMock} />);
    
    // Get the second delete button (for Jane Smith)
    const deleteButtons = screen.getAllByTitle('Delete');
    fireEvent.click(deleteButtons[1]);
    
    expect(onDeleteMock).toHaveBeenCalledTimes(1);
    expect(onDeleteMock).toHaveBeenCalledWith(mockUsers[1].id);
  });
});
