import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './WaitlistForm.module.css';

function WaitlistForm() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      const waitlist = JSON.parse(localStorage.getItem('waitlist') || '[]');
      waitlist.push(email);
      localStorage.setItem('waitlist', JSON.stringify(waitlist));
      setEmail('');
      setMessage('Thanks for joining the waitlist!');
    } else {
      setMessage('Please enter your email address.');
    }
  };

  return (
    <div className={clsx(styles.waitlistContainer, 'glass-card')}>
      <h2>Join Our Waitlist</h2>
      <p>Be the first to know when the book is released!</p>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Your email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit" className="button button--primary">
          Join Waitlist
        </button>
      </form>
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
}

export default WaitlistForm;