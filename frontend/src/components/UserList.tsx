import React from 'react';
import type { User } from '../api';

interface UserListProps {
  users: User[];
  onEdit: (user: User) => void;
  onDelete: (id: string) => void;
}

const UserList: React.FC<UserListProps> = ({ users, onEdit, onDelete }) => {
  return (
    <div className="user-list glass-effect">
      <div className="list-header">
        <h2>Users Directory</h2>
        <span className="badge">{users.length} total</span>
      </div>
      {users.length === 0 ? (
        <div className="empty-state">
          <p>No users found. Create one to get started!</p>
        </div>
      ) : (
        <table className="users-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="fade-in">
                <td>
                  <div className="user-info">
                    <div className="avatar">{user.name.charAt(0).toUpperCase()}</div>
                    <span className="user-name">{user.name}</span>
                  </div>
                </td>
                <td className="user-email">{user.email}</td>
                <td className="actions-cell">
                  <button onClick={() => onEdit(user)} className="btn-icon edit" title="Edit">
                    ✎
                  </button>
                  <button onClick={() => onDelete(user.id)} className="btn-icon delete" title="Delete">
                    🗑
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default UserList;
