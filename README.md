![CI Workflow](https://github.com/vOrcunus/demoapp/workflows/CI%20Workflow/badge.svg)

# DemoApp

This repository contains a sample implementation of a blog application, designed to show off various features of Kubernetes. The blog application is implemented using Python and Django.

In the default deployment configuration, the blog application uses a SQLite database within the container. When using the SQLite database, it will be pre-populated each time the application starts with a set of blog posts. An initial account will also be created for logging into the application to add more posts. The user name for this account is ``developer`` and the password is ``developer``.

Because the SQLite database is stored in the container, new posts and any uploaded images, will be lost when the container restarts. A PostgreSQL database can be attached to the application to add persistence for posts and demonstrate the use of a database. A separate persistent volume can also be attached to the blog application to provide persistent storage for uploaded images. In the case of PostgreSQL being used, a manual step is required to setup the database the first time.

The appearance of the blog application can also be adjusted using a set of environment variables to make it easier to demonstrate blue/green or a/b deployments, split traffic etc. These are:

* ``BLOG_SITE_NAME`` - Sets the title for pages.
* ``BLOG_BANNER_COLOR`` - Sets the color of the page banner

## Bill of Materials (BOM)

This is a list of components that are referred in this repository in order to show off some features of Kubernetes and CI/CD pipelines.

* KinD v1.18.2 (Kubernetes in Docker), a conformant multi-master Kubernetes cluster with the most recent release.
* Harbor v2.0, an OCI-compliant docker registry and chartmuseum for our helm chart.
* Jenkins with Blue Ocean plugin, for automating the build and release processes and demonstrate blue/green deployment.
* A DNS server that serves the hostnames and FQDNs used in this repository.