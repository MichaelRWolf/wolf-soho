#! /usr/bin/perl
#!/usr/bin/perl
use strict;

sub process_file {
  my ($fh) = @_;

  # Discard line 1
  <$fh>;

  # Capture phone number from line 2
  my $line = <$fh>;
  my ($phone_number) = $line =~ /PhoneNumber : (\d+)/;

  # Discard line 3
  <$fh>;

  # Augment headers from line 4
  my $header_line = <$fh>;			
  chomp $header_line;
  print $header_line, "| Phone Number\n";

  # Loop through remaining lines and append phone number
  while (my $line = <$fh>) {
    my $delimiter = q(|);
    chomp($line); 
    my ($sno, $date_and_time, $usage, $type, @junk) = split(q{[|]}, $line);
    my $usage_numy = stringy_to_num($usage);
    print join("|", $sno, $date_and_time, $usage_numy, $type, $phone_number), "\n";
    # print join("|", $line, $phone_number), "\n";
    # print ">", join(',', split(/[|]/, $line)), "\n\n";
  }
}


sub stringy_to_num {
  my ($arg, @junk) = @_;
  die "Extra arg(s): @junk" if @junk;

  my ($num, $units) = split(' ', $arg);
  # print ("arg:@_ => num:$num; units:$units\n");
  return
    $units eq 'KB' ? $num * 1_000 :
    $units eq 'MB' ? $num * 1_000_000 :
    $units eq 'GB' ? $num * 1_000_000_000 :
    warn("Bad units '$units' in arg '$arg'");
}


sub main {
  # Loop through command line arguments
  foreach my $filename (@ARGV) {
    # Open file for read-only access
    open(my $fh, '<', $filename) or die "Failed to open file: $!";
  
    # Pass file handle to process_file subroutine
    process_file($fh);
  
    # Close file handle
    close($fh);
  }
}

main();
