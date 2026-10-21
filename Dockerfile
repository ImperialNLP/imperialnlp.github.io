FROM jekyll/jekyll
LABEL maintainer="Amir Pourmand"
# ImageMagick used to be installed here for the jekyll-imagemagick plugin. That
# plugin has been removed (the site ships pre-generated WebP images), so the
# `convert`/`magick` binaries and their build deps are no longer needed.
WORKDIR /srv/jekyll
# Gemfile.lock is git-ignored, so copy it only when present in the build context.
COPY Gemfile* /srv/jekyll/
RUN bundle install
