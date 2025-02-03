describe package('nginx') do
    it { should be_installed }
end

describe service('nginx') do
    it { should be_running }
    it { should be_enabled }
end

describe file('/var/www/html/index.html') do
    its('content') { should match /Welcome to the DevOps Challenge/ }
end

describe sshd_config do
    its('PermitRootLogin') { should cmp 'no' }
    its('Port') { should cmp '22' }
end

describe user('devops') do
    it { should exist }
    its('groups') { should include 'wheel' }
end
