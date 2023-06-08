import React from 'react'
import styles from './index.module.scss';

export default function Header() {
  return (
      <div className={styles['menu']}>
          <div className={styles['menu-logo']}>LOGO</div>
          <div className={styles['menu-list']}>
          <div className={styles['menu-items']}>Item 1 </div>
          <div className={styles['menu-items']}>Item 2 </div>
          <div className={styles['menu-items']}>Item 3 </div>
          <div className={styles['menu-items']}>Item 4 </div>
          </div>
      </div>
  )
}
