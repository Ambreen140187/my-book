import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/book">
            Start Reading Now
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <section className="container text--center margin-top--lg">
          <div className={clsx('col col--6 col--offset-3', 'glass-card')}>
            <Heading as="h2">Discover the AI-Native Revolution</Heading>
            <p>Dive deep into the future of software development with our comprehensive guide to AI-Native principles, tools, and best practices. Learn how to leverage artificial intelligence to build more intelligent, autonomous, and efficient systems.</p>
            {/* Placeholder for book cover image */}
            <img src="/img/docusaurus.png" alt="AI-Native Book Cover" style={{maxWidth: '200px', margin: '20px auto'}} />
            <Link
              className="button button--primary button--lg"
              to="/book">
              Explore Chapters
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}
