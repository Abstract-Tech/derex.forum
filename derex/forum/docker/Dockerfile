FROM ruby:2.4.1-alpine3.6 as build
MAINTAINER Silvio Tomatis <silviot@gmail.com>

RUN mkdir -p /openedx/forum
RUN apk add --no-cache \
    alpine-sdk \
    bison \
    gdbm-dev \
    libffi-dev \
    linux-headers \
    ncurses-dev \
    openssl-dev \
    readline-dev \
    tar \
    yaml-dev \
    zlib-dev

# Install ruby and some specific dependencies
ENV RUBY_VERSION 2.4.1
ENV BUNDLER_VERSION 1.11.2
ENV RAKE_VERSION 10.4.2
RUN gem install bundler -v $BUNDLER_VERSION
RUN gem install rake -v $RAKE_VERSION
# gem upgrade must come after bundler/rake install
RUN gem install rubygems-update && update_rubygems

# Install forum
RUN wget -O - https://github.com/edx/cs_comments_service/tarball/open-release/ironwood.master|tar xzf - -C /openedx/forum/ --strip-components 1
WORKDIR /openedx/forum
RUN bundle install --deployment

FROM ruby:2.4.1-alpine3.6
MAINTAINER Silvio Tomatis <silviot@gmail.com>

# Not a ruby expert here: we used `dive` to check what files were created in the
# `gem install` build step, and copy them here
COPY --from=build /openedx/forum /openedx/forum
COPY --from=build /usr/local/bundle/bin /usr/local/bundle/bin
COPY --from=build /usr/local/bundle/config /usr/local/bundle/config

ENV RACK_ENV staging
ENV NEW_RELIC_ENABLE false
ENV API_KEY forumapikey
ENV SEARCH_SERVER "http://elasticsearch:9200"
ENV MONGODB_AUTH ""
ENV MONGODB_HOST mongodb
ENV MONGODB_PORT 27010
ENV MONGODB_DB derex_forum

ENV MONGOHQ_URL "mongodb://$MONGODB_AUTH$MONGODB_HOST:$MONGODB_PORT/$MONGODB_DB"
EXPOSE 4567
CMD /openedx/forum/bin/unicorn -c config/unicorn_tcp.rb -I '.'
