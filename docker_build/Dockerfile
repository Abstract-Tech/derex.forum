ARG RUBY_VERSION=2.5.7
FROM ruby:${RUBY_VERSION}
LABEL maintainer="Chiruzzi Marco <chiruzzi.marco@gmail.com>"

RUN apt-get update && apt-get install git

# Throw errors if Gemfile has been modified since Gemfile.lock
RUN bundle config --global frozen 1

# Upgrade bundler to the Gemfile specified version
RUN gem install bundler -v 1.16.6

ARG FORUM_VERSION=open-release/koa.master
ARG FORUM_REPOSITORY=https://github.com/edx/cs_comments_service.git

RUN git clone ${FORUM_REPOSITORY} --branch ${FORUM_VERSION} --depth 1 /openedx/forum
WORKDIR /openedx/forum

# Juniper release enforce authentication on the MongoDB database
# We are needing it on previous releases too
COPY mongoid.yml /openedx/forum/config/mongoid.yml

RUN bundle install --deployment

# This have any real effect only if set to "development"
# https://github.com/edx/cs_comments_service/blob/open-release/koa.master/app.rb#L154
ENV RACK_ENV production

ENV NEW_RELIC_ENABLE false
ENV API_KEY forumapikey
ENV SEARCH_SERVER "http://elasticsearch:9200"
ENV MONGOHQ_URL "mongodb://root:secret@mongodb:27017/derex_forum"
ENV MONGOID_AUTH_MECH=":scram"
ENV MONGOID_AUTH_SOURCE="admin"
EXPOSE 4567
CMD /openedx/forum/bin/unicorn -c config/unicorn_tcp.rb -I '.'

ENV DEREX_FORUM_VERSION=0.2.2
