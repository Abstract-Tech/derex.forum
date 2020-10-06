FROM ruby:2.5.7
LABEL maintainer="Chiruzzi Marco <chiruzzi.marco@gmail.com>"

# Throw errors if Gemfile has been modified since Gemfile.lock
RUN bundle config --global frozen 1

# Upgrade bundler to the Gemfile specified version
RUN gem install bundler -v 1.16.6

RUN mkdir -p /openedx/forum
WORKDIR /openedx/forum

RUN wget -O - \
    https://github.com/edx/cs_comments_service/tarball/open-release/juniper.master | \
    tar xzf - --strip-components 1
RUN bundle install --deployment

ENV RACK_ENV staging
ENV NEW_RELIC_ENABLE false
ENV API_KEY forumapikey
ENV SEARCH_SERVER "http://elasticsearch:9200"
# Juniper release enforce authentication on the MongoDB database
ENV MONGOHQ_URL "mongodb://root:secret@mongodb:27017/derex_forum"
ENV MONGOID_AUTH_MECH=":scram"
ENV MONGOID_AUTH_SOURCE="admin"
EXPOSE 4567
CMD /openedx/forum/bin/unicorn -c config/unicorn_tcp.rb -I '.'
