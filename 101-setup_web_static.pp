# Configures a web server for deployment of web_static.

# Nginx configuration file
file { '/data/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases/':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/shared/':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases/test/':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

file { '/data/web_static/current/index.html':
  ensure  => 'file',
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n',
}

service { 'nginx':
  ensure => 'running',
}
