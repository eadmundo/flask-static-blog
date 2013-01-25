class vagrant::puppet {
  # Symlink the weird vagrant Puppet location to the normal system location
  file { '/usr/bin/puppet':
    ensure => link,
    target => '/opt/vagrant_ruby/bin/puppet',
  }
}
