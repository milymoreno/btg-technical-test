import { useEffect, useState } from 'react';
import { userApi, type User, type UserCreate, type UserUpdate } from './api';
import UserList from './components/UserList';
import UserForm from './components/UserForm';

function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = async () => {
    try {
      const data = await userApi.getUsers();
      setUsers(data);
      setError(null);
    } catch (err) {
      console.error("Failed to fetch users", err);
      setError("Failed to connect to the server. Please ensure the backend is running.");
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleCreate = async (data: UserCreate | UserUpdate) => {
    try {
      await userApi.createUser(data as UserCreate);
      setIsFormOpen(false);
      fetchUsers();
    } catch (err) {
      console.error("Error creating user", err);
      setError("Failed to create user.");
    }
  };

  const handleUpdate = async (data: UserCreate | UserUpdate) => {
    if (!editingUser) return;
    try {
      await userApi.updateUser(editingUser.id, data as UserUpdate);
      setEditingUser(undefined);
      setIsFormOpen(false);
      fetchUsers();
    } catch (err) {
      console.error("Error updating user", err);
      setError("Failed to update user.");
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    try {
      await userApi.deleteUser(id);
      fetchUsers();
    } catch (err) {
      console.error("Error deleting user", err);
      setError("Failed to delete user.");
    }
  };

  const openCreateForm = () => {
    setEditingUser(undefined);
    setIsFormOpen(true);
  };

  const openEditForm = (user: User) => {
    setEditingUser(user);
    setIsFormOpen(true);
  };

  return (
    <div className="app-container">
      <header className="app-header glass-effect">
        <div className="logo-container">
          <div className="logo-icon">✨</div>
          <h1>User Management Hub</h1>
        </div>
        <button onClick={openCreateForm} className="btn-primary">
          + New User
        </button>
      </header>
      
      <main className="main-content">
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            <p>{error}</p>
          </div>
        )}
        
        <UserList 
          users={users} 
          onEdit={openEditForm} 
          onDelete={handleDelete} 
        />
      </main>

      {isFormOpen && (
        <UserForm 
          initialData={editingUser} 
          onSubmit={editingUser ? handleUpdate : handleCreate} 
          onCancel={() => {
            setIsFormOpen(false);
            setEditingUser(undefined);
          }} 
        />
      )}
    </div>
  );
}

export default App;
